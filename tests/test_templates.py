from os import path
from pydantic import FilePath

from tests.conftest import CONFIG_PAGES, CONFIG_TEMPLATES, StepEnum
from consentforms import images as i
from consentforms import templates as t


def test_find_best_template(tmp_path, crop_img_files):
    svg_template_filepath = t.find_best_template(crop_img_files.files.get(StepEnum.CROPPED).path,
                                                 CONFIG_PAGES,
                                                 CONFIG_TEMPLATES)
    assert svg_template_filepath is not None
    assert svg_template_filepath is not ""


def test_not_find_best_template(tmp_path, base_img_files):
    # TODO improve test using a image that could be a consent form
    folder = base_img_files.files.get(StepEnum.ROTATED).path.parent
    root_filename = base_img_files.files.get(StepEnum.ROTATED).path.stem.split(i.CONVERT_PAGE_SEPARATOR)
    img_filepath = path.join(folder, f"{root_filename}{i.CONVERT_PAGE_SEPARATOR}0{i.CONVERT_PNG_EXT}")
    svg_template_filepath = t.find_best_template(FilePath(img_filepath),
                                                 CONFIG_PAGES,
                                                 CONFIG_TEMPLATES)
    assert svg_template_filepath is None

