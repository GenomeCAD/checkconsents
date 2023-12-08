#!/usr/bin/env python3

import argparse
from datetime import datetime
from enum import Enum, IntEnum
from functools import cached_property
from glob import glob
import json
import os
from pathlib import Path
import tempfile
import jsonschema
import logging
from  os import system, popen, path, remove
from prettyprinter import pprint, pformat
from pydantic import BaseModel, ConfigDict, DirectoryPath, Field, FilePath, PositiveInt, ValidationError, computed_field, conint, field_validator, validator
from schema import Schema, SchemaError
import shutil
from typing import Dict, List, Tuple, Optional
import yaml

import detect_orientation
import detect_checkboxes
import detect_correct_template
import simpleomr
import logutils


__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@genomecad.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GLP3"
__version__ = '1.0.1'
__prog_name__ = 'CheckConsents'

UNDERTERMINED = 'undertermined'


def version():
    return __version__


def prog_name():
    return __prog_name__


def arguments_parser():
    '''
    Arguments parsing.

    :return: Object
    '''
    parser = argparse.ArgumentParser(description='Check consent checkboxes into consent forms (pdf format)',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--version', action='version', version=version())


    inputs = parser.add_argument_group('Inputs')
    inputs.add_argument('-i', '--input_folder',
                        type=str,
                        help='path of input directory',
                        required=True)
    inputs.add_argument("-w", "--working_dir",
                        type=str,
                        default="/tmp",
                        help="Directory use to generate intermediates",
                        required=False)

    config = parser.add_argument_group('Config')
    config.add_argument('--configfile',
                        type=str,
                        default=path.join(path.dirname(__file__), 
                                          'checkconsents_config.yml'),
                        help='configfile filepath',
                        required=False)

    logger_arguments = parser.add_argument_group('Logger')
    logger_arguments.add_argument('--log_level',
                                  type=str,
                                  default='INFO',
                                  help='log level',
                                  choices=['ERROR', 'error', 'WARNING', 'warning',
                                           'INFO', 'info', 'DEBUG', 'debug'],
                                  required=False)
    logger_arguments.add_argument('--log_file',
                                  type=str,
                                  help='log file (use the stderr by default)',
                                  required=False)
    return parser


class PdfConvertError(Exception):
    def __init__(self, message: str):
        super.__init__(message)


class OmrError(Exception):
    def __init__(self, message: str):
        super.__init__(message)


class ExitCode(IntEnum):
    FINE = 0
    INPUT_DIR_NOT_EXIST = 1
    PDF_CONVERT = 2
    OMR_ERROR = 3
    ERROR = 10


class Consent(BaseModel):
    omr_res : List[simpleomr.OmrResult]
    pdf_filepath: FilePath
    debug_img_filepath: Optional[FilePath] = None
    

    @computed_field(return_type=str)
    @cached_property
    def consent(self):
        msg = "Can not resolve the consent, a debug image is required"
        if len(self.omr_res) != 2:
            raise Exception(message="the size of OMR result list is expected to be 2")
        
        d = {simpleomr.OmrValueEnum.CHECKED: [simpleomr.OmrValueEnum.EMPTY],
             simpleomr.OmrValueEnum.FILLED: [simpleomr.OmrValueEnum.EMPTY],
             simpleomr.OmrValueEnum.EMPTY: [simpleomr.OmrValueEnum.CHECKED, 
                                            simpleomr.OmrValueEnum.FILLED]}
        resolvable = False
        area_id = None
        a = self.omr_res[0]
        b = self.omr_res[1]
        logger = logging.getLogger(path.basename(__prog_name__))
        logger.debug(a.value)
        logger.debug(b.value)
        logger.debug(d.keys())
        if a.value in d.keys():
            if a.value != simpleomr.OmrValueEnum.EMPTY:
                area_id = a.template_search_area_id
            for v in d[a.value]:
                if b.value == v:
                    resolvable = True
                    if area_id is None: 
                        area_id = b.template_search_area_id
        if resolvable:
            return area_id
        else:
            return UNDERTERMINED


class ConvertParams(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    density: Optional[int] = 300
    opt_args: Optional[str] = None

    @field_validator('density')
    def set_density(cls, density):
        return density or 300
    

class Config(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    
    intermediates : bool
    templates: Dict[str, detect_correct_template.Template]
    pages: Dict[str, str]
    conversion: Optional[ConvertParams] = ConvertParams()
    parsing_header_limit: Optional[conint(gt=0)] = 5

    @field_validator('conversion')
    def set_conversion(cls, conversion):
        return conversion or ConvertParams()
    
    @field_validator('parsing_header_limit')
    def set_convert(cls, parsing_header_limit):
        return parsing_header_limit or 5


def load_yaml(yaml_file_path: str):
    with open(yaml_file_path, 'r') as yaml_file:
        data_content = yaml.safe_load(yaml_file)
    return data_content


def default_config_schema():
    return Config.model_json_schema()


def load_config(conf_yaml_filepath: str, config_schema=default_config_schema()) -> Config:
    c = load_yaml(conf_yaml_filepath)
    try:
        jsonschema.validate(c, config_schema)
        return Config(**c)
    except ValidationError as ve:
        raise ve
    

def cleaning(fpath,
             logger=None):
    """
    Clean temporary data generated during execution

    :param fpath: absolute path of directory or file to remove
    :type fpath: str
    :param logger: logger object, defaults to None
    :type logger: Logger, optional
    :return: True if an action is performed and False if no aciton is performed
    :rtype: Boolean
    """

    if not logger:
        logger = logging.getLogger(cleaning.__name__)
    if path.exists(fpath):
        logger.debug("Cleaning {}".format(fpath))
        if path.isfile(fpath):
            remove(fpath)
        elif path.isdir(fpath):
            shutil.rmtree(fpath)
        else:
            logger.warn("cleaning function does not handle the type of {}".format(fpath))
            logger.warn("Nothing done")
            return False
        logger.debug("{} deleted".format(fpath))
        return True
    else:
        logger.debug("{} does not exist. Nothing to do".format(fpath))
        return False

def convert_pdf_2_png(pdf_filepath: FilePath, 
                      png_filepath: FilePath, 
                      density: int = 300, 
                      optional_args: str = None):
    tool = "convert"
    cmd_args = f"-density {density} {pdf_filepath.resolve()} {png_filepath.resolve()}"
    cmd = [tool, cmd_args]
    if optional_args is not None:
        cmd.insert(1, optional_args)
    exit_code = system(' '.join(cmd))
    if exit_code != 0:
        raise PdfConvertError(f"Conversion of {pdf_filepath.resolve} failed")
    return exit_code
    # stream = os.popen(f"convert -density {density} {pdf_filepath.resolve()} {png_filepath.resolve()}")
    # return stream.read()


def image_correction(png_filepath: FilePath) -> FilePath:
    abs_filename, file_ext = path.splitext(png_filepath.resolve())
    img_mat = detect_orientation.image_2_Mat(png_filepath)
    osd = detect_orientation.image_2_osd(img_mat)
    img_corrected_path = f"{abs_filename}-corrected.png"
    detect_orientation.rotate_image(img_mat, osd["rotate"], img_corrected_path)
    return Path(img_corrected_path)


def crop_image(png_filepath: FilePath) -> FilePath:
    abs_filename, file_ext = path.splitext(png_filepath.resolve())
    img_mat = detect_orientation.image_2_Mat(png_filepath)
    cropped_img_filepath = f"{abs_filename}-cropped.png"
    if detect_checkboxes.generate_crop_image(img_mat, cropped_img_filepath):
        return Path(cropped_img_filepath)
    else:
        return None
    

def get_template(png_filepath: FilePath, pages: dict, templates: dict, parsing_header_limit: int) -> str:
    return detect_correct_template.find_best_template(png_filepath, pages, templates, parsing_header_limit)


def omr(img: Path, svg_template: Path):
    logger = logging.getLogger(path.basename(__prog_name__))
    logger.debug(f"img {img.resolve()}, svg_template {svg_template.resolve()}")
    if img.exists() and svg_template.exists():
        logger.debug("load image")
        image = simpleomr.load_image(img.resolve())
        logger.debug("get marks")
        marks = simpleomr.load_svg_rects(svg_template.resolve(), image.shape)
        if len(marks) == 0:
            raise simpleomr.OmrTemplateError(svg_template.resolve(), "template contains no marks")
        logger.debug("clean image")
        clean = simpleomr.clean_image(image)
        logger.debug("scan marks")
        res = simpleomr.scan_marks(clean, marks)
        logger.debug(f"res: {res}")
        return res, image, clean, marks
    return None


def create_debug_image(output_filepath: str, image, clean, marks, res):
    simpleomr.debug_marks(output_filepath, image, clean, marks, res)


def main(args):
    exec_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    # Set logger
    logger = logutils.setup_logger(path.basename(__prog_name__), args.log_level.upper(), args.log_file)

    # load config file:
    config = load_config(args.configfile)

    logger.debug(f"configuration: {pformat(config.model_dump())}")
    logger.info("Start processing...")
    
    input_dir = Path(args.input_folder)
    if not input_dir.exists():
        logger.error("Input folder does not exist")
        return 1
    if not input_dir.is_dir():
        logger.error("Incorrect Input folder (not a directory)")
        return 1
    
    try:
        errors_pdf_convert: List[str] = []
        errors_omr: List[str] = []

        consents: List[Consent] = []
        output_dir_path = DirectoryPath(path.join(args.working_dir, f"{__prog_name__}_{exec_time}"))
        output_file_path = FilePath(path.join(output_dir_path, "consents.json"))
        
        logger.info(f"Create output directory: {output_dir_path}")
        os.makedirs(output_dir_path, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=output_dir_path, delete=not config.intermediates) as tmpdirname:  
            logger.info(f"Working directory: {tmpdirname}")
            #TODO parallel tasks / subprocess / thread
            for pf in glob(path.join(input_dir.resolve(), "*.pdf")):
                file_name, _ = path.splitext(path.basename(pf))
                logger.debug(f"pdf: {pf}")
                logger.debug(f"pdf: {path.basename(pf)}")
                logger.info("Convert pdf to png")
                img_file_path = Path(path.join(tmpdirname, f"{file_name}.png"))
                exit_code = convert_pdf_2_png(Path(pf), 
                                            img_file_path, 
                                            config.conversion.density, 
                                            config.conversion.opt_args)
                if exit_code != 0:
                    msg = f"Error during pdf conversion: {pf}"
                    logger.error(msg)
                    errors_pdf_convert.append(msg)
                
                logger.info("detect orientation - generate corrected image")

                logger.debug(popen(f"ls -la {tmpdirname}").read())
                
                for img in glob(path.join(tmpdirname, f"{file_name}-*.png")):
                    img_path = Path(img)
                    img_corrected_path = image_correction(img_path)
                    img_cropped_path = crop_image(img_corrected_path)
                    svg_template_filepath = get_template(img_cropped_path, 
                                                        config.pages, 
                                                        config.templates, 
                                                        config.parsing_header_limit)
                    logger.debug(popen(f"ls -la {tmpdirname}").read())
                    if svg_template_filepath is None:
                        logger.debug(f"{img_path} - no template")
                        continue
                    try:
                        svg_template_path = Path(svg_template_filepath)
                        res, image, clean, marks = omr(img_cropped_path, svg_template_path)
                        logger.info(f"OMR results ({img_path}): {res}")
                        consent = Consent(pdf_filepath=FilePath(pf), omr_res=res)
                        if consent.consent == UNDERTERMINED or logger.isEnabledFor(logging.DEBUG):
                            img_cropped_filename, _ = path.splitext(path.basename(img_cropped_path.resolve()))
                            debug_image_filepath = path.join(output_dir_path, f"{img_cropped_filename}-omr-debug.png")
                            create_debug_image(debug_image_filepath, image, clean, marks, res)
                            consent.debug_img_filepath = FilePath(debug_image_filepath)
                        consents.append(consent)
                    except simpleomr.OmrTemplateError as e:
                        logger.error(e)
                        msg = f"Error during OMR: {img_cropped_path.resolve()}[{e}]"
                        logger.error(msg)
                        errors_omr.append(msg)
        logger.info("Final results:")
        logger.info(pformat(consents))
        indent = 4 if logger.isEnabledFor(logging.DEBUG) else None
        with open(output_file_path.resolve(), 'w') as f:
            json.dump([c.model_dump(mode='json') for c in consents], f, indent=indent)
        logger.debug(popen(f"ls -lah {output_dir_path}").read())

        if len(errors_pdf_convert) != 0 or len(errors_omr) != 0:
            logger.warn("Some error have been raised during the execution refer to log for further details")
        if len(errors_pdf_convert) != 0:
            msg = ', '.join(errors_pdf_convert)
            raise PdfConvertError(msg)
        if len(errors_omr) != 0:
            msg = ', '.join(errors_omr)
            raise OmrError(msg)
        
    except PdfConvertError as e:
        logger.error(e)
        return ExitCode.PDF_CONVERT
    except OmrError as e:
        logger.error(e)
        return ExitCode.OMR_ERROR
    except Exception as e:
        logger.error(e)
        return ExitCode.ERROR
    else:
        return ExitCode.FINE #TODO handle wrong exit / doc of exit values : 1, 2, 3
    finally:
        logger.info("process done")


if __name__ == '__main__':
    args = arguments_parser().parse_args()
    exit(main(args))

