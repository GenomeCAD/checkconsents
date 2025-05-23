#!/usr/bin/env python3

__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@inserm.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GNU AGLP3"
__version__ = "1.3.0"
__prog_name__ = "CheckConsents"

import argparse
from datetime import datetime
from enum import IntEnum
from functools import cached_property
from glob import glob
import json
import os
from pathlib import Path
import tempfile
import jsonschema
import logging
from os import popen, path, remove
from prettyprinter import pformat
from pydantic import BaseModel, ConfigDict, DirectoryPath, FilePath, ValidationError, computed_field, conint, \
    field_validator
from pytesseract import TesseractError 
import shutil
from typing import Dict, List, Optional
import yaml

import sys
sys.path.append(path.join(path.dirname(__file__), ".."))
from consentforms import omr, templates, images, logutils


UNDERTERMINED = "undertermined"


def version():
    return __version__


def prog_name():
    return __prog_name__


def arguments_parser():
    """
    Arguments parsing.

    :return: Object
    """
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


class OmrError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ExitCode(IntEnum):
    FINE = 0
    INPUT_DIR_NOT_EXIST = 1
    PDF_CONVERT = 2
    OMR_ERROR = 3
    ERROR = 10


class Consent(BaseModel):
    omr_res: List[omr.OmrResult]
    pdf_filepath: FilePath
    debug_img_filepath: Optional[FilePath] = None

    @computed_field(return_type=str)
    @cached_property
    def consent(self):
        msg = "Can not resolve the consent, a debug image is required"
        if len(self.omr_res) != 2:
            raise Exception("the size of OMR result list is expected to be 2")
        d = {omr.OmrValueEnum.CHECKED: [omr.OmrValueEnum.EMPTY],
             omr.OmrValueEnum.FILLED: [omr.OmrValueEnum.EMPTY],
             omr.OmrValueEnum.EMPTY: [omr.OmrValueEnum.CHECKED,
                                      omr.OmrValueEnum.FILLED]}
        resolvable = False
        area_id = None
        a = self.omr_res[0]
        b = self.omr_res[1]
        logger = logging.getLogger(path.basename(__prog_name__))
        logger.debug(a.value)
        logger.debug(b.value)
        logger.debug(d.keys())
        if a.value in d.keys():
            if a.value != omr.OmrValueEnum.EMPTY:
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

    intermediates: bool
    templates: Dict[str, templates.Template]
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


def load_config(conf_yaml_filepath: str, config_schema=None) -> Config:
    if config_schema is None:
        config_schema = default_config_schema()
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
            logger.warning("cleaning function does not handle the type of {}".format(fpath))
            logger.warning("Nothing done")
            return False
        logger.debug("{} deleted".format(fpath))
        return True
    else:
        logger.debug("{} does not exist. Nothing to do".format(fpath))
        return False


def image_correction(png_filepath: FilePath) -> FilePath:
    abs_filename, file_ext = path.splitext(png_filepath.resolve())
    img_mat = images.image_2_mat(png_filepath)
    osd = images.image_2_osd(img_mat)
    img_corrected_path = f"{abs_filename}-corrected.png"
    images.rotate_image(img_mat, osd["rotate"], img_corrected_path)
    return Path(img_corrected_path)


def crop_image(png_filepath: FilePath) -> FilePath:
    abs_filename, file_ext = path.splitext(png_filepath.resolve())
    img_mat = images.image_2_mat(png_filepath)
    cropped_img_filepath = f"{abs_filename}-cropped.png"
    if images.generate_crop_image(img_mat, cropped_img_filepath):
        return Path(cropped_img_filepath)
    else:
        return None


def get_template(png_filepath: FilePath,
                 pages: Dict[str, str],
                 tpls: Dict[str, templates.Template],
                 parsing_header_limit: int) -> str:
    return templates.find_best_template(png_filepath, pages, tpls, parsing_header_limit)


def optical_mark_reco(img: Path, svg_template: Path):
    logger = logging.getLogger(path.basename(__prog_name__))
    logger.debug(f"img {img.resolve()}, svg_template {svg_template.resolve()}")
    if img.exists() and svg_template.exists():
        logger.debug("load image")
        image = omr.load_image(str(img.resolve()))
        logger.debug("get marks")
        marks = omr.load_svg_rects(svg_template.resolve(), image.shape)
        if len(marks) == 0:
            raise omr.OmrTemplateError(svg_template.resolve(), "template contains no marks")
        logger.debug("clean image")
        clean = omr.clean_image(image)
        logger.debug("scan marks")
        res = omr.scan_marks(clean, marks)
        logger.debug(f"res: {res}")
        return res, image, clean, marks
    return None


def create_debug_image(output_filepath: str, image, clean, marks, res):
    omr.debug_marks(output_filepath, image, clean, marks, res)


def main(cli_args):
    exec_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    # Set logger
    logger = logutils.setup_logger(path.basename(__prog_name__), cli_args.log_level.upper(), cli_args.log_file)

    # load config file:
    config = load_config(cli_args.configfile)

    logger.debug(f"configuration: {pformat(config.model_dump())}")
    logger.info("Start processing...")

    input_dir = Path(cli_args.input_folder)
    if not input_dir.exists():
        logger.error("Input folder does not exist")
        return 1
    if not input_dir.is_dir():
        logger.error("Incorrect Input folder (not a directory)")
        return 1

    try:
        errors_pdf_convert: List[str] = []
        errors_img_analysis: List[str] = []
        errors_omr: List[str] = []

        consents: List[Consent] = []
        output_dir_path = DirectoryPath(path.join(cli_args.working_dir, f"{__prog_name__}_{exec_time}"))
        output_file_path = FilePath(path.join(output_dir_path, "consents.json"))

        logger.info(f"Create output directory: {output_dir_path}")
        os.makedirs(output_dir_path, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=output_dir_path, delete=not config.intermediates) as tmpdirname:
            logger.info(f"Working directory: {tmpdirname}")
            # TODO parallel tasks / subprocess / thread
            for pf in glob(path.join(input_dir.resolve(), "*.pdf")):
                file_name, _ = path.splitext(path.basename(pf))
                logger.debug(f"pdf: {pf}")
                logger.debug(f"pdf: {path.basename(pf)}")
                logger.info("Convert pdf to png")
                img_file_path = Path(path.join(tmpdirname, f"{file_name}.png"))
                try:
                    images.convert_pdf_2_png(Path(pf),
                                             DirectoryPath(tmpdirname),
                                             images.default_convert_output_format(file_name),
                                             config.conversion.density,
                                             config.conversion.opt_args)
                except images.PdfConvertError as pce:
                    logger.error(pce)
                    errors_pdf_convert.append(pce)
                    continue

                logger.info("detect orientation - generate corrected image")

                logger.debug(popen(f"ls -la {tmpdirname}").read())

                for img in glob(path.join(tmpdirname, f"{file_name}{images.CONVERT_PAGE_SEPARATOR}*.png")):
                    img_path = Path(img)
                    try:
                        img_corrected_path = image_correction(img_path)
                        img_cropped_path = crop_image(img_corrected_path)
                        svg_template_filepath = get_template(img_cropped_path,
                                                            config.pages,
                                                            config.templates,
                                                            config.parsing_header_limit)
                    except TesseractError as te:
                        msg = f"({img}) " + te
                        logger.error(msg)
                        errors_img_analysis.append(msg)
                        continue
                    except templates.FindTemplateError as fte:
                        logger.error(fte)
                        errors_img_analysis.append(fte)
                        continue
                    logger.debug(popen(f"ls -la {tmpdirname}").read())
                    if svg_template_filepath is None:
                        logger.debug(f"{img_path} - no template")
                        continue
                    try:
                        svg_template_path = Path(svg_template_filepath)
                        res, image, clean, marks = optical_mark_reco(img_cropped_path, svg_template_path)
                        logger.info(f"OMR results ({img_path}): {res}")
                        consent = Consent(pdf_filepath=FilePath(pf), omr_res=res)
                        if consent.consent == UNDERTERMINED or logger.isEnabledFor(logging.DEBUG):
                            img_cropped_filename, _ = path.splitext(path.basename(img_cropped_path.resolve()))
                            debug_image_filepath = path.join(output_dir_path, f"{img_cropped_filename}-omr-debug.png")
                            create_debug_image(debug_image_filepath, image, clean, marks, res)
                            consent.debug_img_filepath = FilePath(debug_image_filepath)
                        consents.append(consent)
                    except omr.OmrTemplateError as e:
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

        if len(errors_pdf_convert) != 0 or len(errors_img_analysis) != 0 or len(errors_omr) != 0:
            logger.warning("Some error have been raised during the execution refer to log for further details")
        if len(errors_pdf_convert) != 0:
            msg = ', '.join(errors_pdf_convert)
            raise images.PdfConvertError(msg)
        if len(errors_img_analysis) != 0 :
            msg = ', '.join(errors_img_analysis)
            raise Exception(msg)
        if len(errors_omr) != 0:
            msg = ', '.join(errors_omr)
            raise OmrError(msg)

    except images.PdfConvertError as e:
        logger.error(e)
        return ExitCode.PDF_CONVERT
    except OmrError as e:
        logger.error(e)
        return ExitCode.OMR_ERROR
    except Exception as e:
        logger.error(e)
        return ExitCode.ERROR
    else:
        return ExitCode.FINE
    finally:
        logger.info("process done")


if __name__ == '__main__':
    args = arguments_parser().parse_args()
    exit(main(args))
