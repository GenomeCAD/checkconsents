from enum import IntEnum
from os import path
from pydantic import FilePath, BaseModel, DirectoryPath
import pytest
import shutil
import sys
from typing import Dict, Optional

from consentforms.images import convert_pdf_2_png, image_2_mat, rotate_image, generate_crop_image, default_convert_output_format
from consentforms.logutils import setup_logger
from consentforms.templates import Template, find_best_template


PDF_FILE_NAME = "functests_consent.pdf"
PDF_PAGES_ROTATED_FILE_NAME = "functests_consent_rotated.pdf"
PNG_FILE_NAME = "functests_consent.png"
PNG_ROTATED_FILE_NAME = "functests_consent_rotated.png"
PNG_CROPPED_FILE_NAME = "functests_consent_cropped.png"
DATA_FOLDER_NAME = "data"

TEMPLATES_DIR_PATH = DirectoryPath(path.join(path.dirname(__file__), "../resources/all_templates"))
TEMPLATE_FILE_NAME = "mineur_decede.svg"
TEMPLATE_FILEPATH = FilePath(path.join(TEMPLATES_DIR_PATH.resolve(), TEMPLATE_FILE_NAME))
TEMPLATE2_FILEPATH = FilePath(path.join(TEMPLATES_DIR_PATH.resolve(), "mineur.svg"))
PDF_FILEPATH = FilePath(path.join(path.dirname(__file__), "resources/initial_data/Consentement_1.pdf"))
PDF_PAGES_ROTATED_FILEPATH = FilePath(path.join(path.dirname(__file__), "resources/initial_data_extra/Consentement_tweaked_1.pdf"))
CONFIG_PAGES = {"recherche": "Consentement pour la conservation, dans un but de recherche"}
CONFIG_TEMPLATES = {
    "test": Template(pattern="génétiques d’une personne mineure décédée",
                     path=TEMPLATE_FILEPATH,
                     priority=1),
    "test2": Template(pattern="génétiques d’une personne mineure réalisé pour une finalité médicale",
                      path=TEMPLATE2_FILEPATH,
                      priority=1)
}

# IMG_FILEPATH = FilePath(path.join(path.dirname(__file__), "resources/consentement-1-3.png"))
# ROTATED_IMG_FILEPATH = FilePath(path.join(path.dirname(__file__), "resources/consentement-1-3_rotated.png"))

TEST_LOGGER = setup_logger("Test", "debug")


class StepEnum(IntEnum):
    BASE = 0,
    ROTATED = 1,
    CROPPED = 2,
    TEMPLATE = 3


class TestingFile(BaseModel):
    name: str
    path: FilePath


class TestingData(BaseModel):
    files: Optional[Dict[StepEnum, TestingFile]] = {}
    form_page: Optional[TestingFile] = None


@pytest.fixture(scope="session")
def pdf_file(tmp_path_factory):
    tmp_filepath = path.join(tmp_path_factory.mktemp(DATA_FOLDER_NAME), PDF_FILE_NAME)
    shutil.copy(PDF_FILEPATH, tmp_filepath)
    return tmp_filepath


@pytest.fixture(scope="session")
def base_img_files(tmp_path_factory, pdf_file):
    dirname = path.dirname(pdf_file)
    file_name, _ = path.splitext(path.basename(pdf_file))
    convert_pdf_2_png(FilePath(pdf_file),
                      DirectoryPath(dirname),
                      default_convert_output_format(file_name))
    data = TestingData()
    data.form_page = TestingFile(name=f"{file_name}-3.png",
                                 path=FilePath(path.join(dirname, f"{file_name}-3.png")))
    data.files[StepEnum.BASE] = data.form_page
    return data


@pytest.fixture(scope="session")
def rotate_img_files(tmp_path_factory, base_img_files):
    data = base_img_files
    img = image_2_mat(data.form_page.path.resolve())
    rotated_img_filepath = path.join(data.form_page.path.parent.resolve(), PNG_ROTATED_FILE_NAME)
    rotate_image(img, 180, rotated_img_filepath)
    data.files[StepEnum.ROTATED] = TestingFile(name=path.basename(rotated_img_filepath),
                                               path=FilePath(rotated_img_filepath))
    return data


@pytest.fixture(scope="session")
def crop_img_files(tmp_path_factory, base_img_files):
    data = base_img_files
    rtf = data.files.get(StepEnum.BASE)
    cropped_img_filepath = path.join(rtf.path.parent, PNG_CROPPED_FILE_NAME)
    if generate_crop_image(image_2_mat(rtf.path), cropped_img_filepath):
        data.files[StepEnum.CROPPED] = TestingFile(name=PNG_CROPPED_FILE_NAME, path=FilePath(cropped_img_filepath))
    return data


@pytest.fixture(scope="session")
def template_files(tmp_path_factory, crop_img_files):
    data = crop_img_files
    svg_template_filepath = find_best_template(data.files.get(StepEnum.CROPPED).path,
                                               CONFIG_PAGES,
                                               CONFIG_TEMPLATES)
    data.files[StepEnum.TEMPLATE] = TestingFile(name=TEMPLATE_FILE_NAME, path=FilePath(svg_template_filepath))
    return data
