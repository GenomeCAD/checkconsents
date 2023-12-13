from pydantic import FilePath

from consentforms import omr
from consentforms.omr import OmrValueEnum
from tests.conftest import StepEnum, TEST_LOGGER
from consentforms.checkconsents import UNDERTERMINED, Consent


def test_scan_marks(tmp_path, template_files):
    svg_template = template_files.files.get(StepEnum.TEMPLATE).path.resolve()
    image = omr.load_image(str(template_files.files.get(StepEnum.CROPPED).path.resolve()))
    marks = omr.load_svg_rects(svg_template, image.shape)
    assert len(marks) != 0

    clean = omr.clean_image(image)
    res = omr.scan_marks(clean, marks)
    assert len(res) == 2

    checked_res = [r for r in res if r.value == OmrValueEnum.CHECKED]
    empty_res = [r for r in res if r.value == OmrValueEnum.EMPTY]
    assert len(checked_res) == 1
    assert checked_res[0].pixel_constituent > 0
    assert len(empty_res) == 1
    assert empty_res[0].pixel_constituent == 0


def test_consent_class(pdf_file):
    box_id1 = 'box1'
    box_id2 = 'box2'

    res_empty = omr.OmrResult(template_search_area_id=box_id1, value=omr.OmrValueEnum.EMPTY, pixel_constituent=0.0)
    res_checked = omr.OmrResult(template_search_area_id=box_id1, value=omr.OmrValueEnum.CHECKED, pixel_constituent=0.2)
    res_filled = omr.OmrResult(template_search_area_id=box_id1, value=omr.OmrValueEnum.FILLED, pixel_constituent=0.9)

    res_empty2 = omr.OmrResult(template_search_area_id=box_id2, value=omr.OmrValueEnum.EMPTY, pixel_constituent=0.0)
    res_checked2 = omr.OmrResult(template_search_area_id=box_id2, value=omr.OmrValueEnum.CHECKED, pixel_constituent=0.2)
    res_filled2 = omr.OmrResult(template_search_area_id=box_id2, value=omr.OmrValueEnum.FILLED, pixel_constituent=0.9)

    # case box1 checked box2 empty
    TEST_LOGGER.info(type(res_checked))
    TEST_LOGGER.info(omr.OmrResult.model_validate(res_checked))

    c = Consent(pdf_filepath=FilePath(pdf_file), omr_res=[res_checked, res_empty2])
    assert c.consent == box_id1
    c = Consent(pdf_filepath=FilePath(pdf_file), omr_res=[res_empty2, res_checked])
    assert c.consent == box_id1

    # case box1 checked box2 filled
    c = Consent(pdf_filepath=FilePath(pdf_file), omr_res=[res_checked, res_filled2])
    assert c.consent == UNDERTERMINED

    # case box1 checked box2 checked
    c = Consent(pdf_filepath=FilePath(pdf_file), omr_res=[res_checked, res_checked2])
    assert c.consent == UNDERTERMINED

    # case box1 empty box2 empty
    c = Consent(pdf_filepath=FilePath(pdf_file), omr_res=[res_empty, res_empty2])
    assert c.consent == UNDERTERMINED

    # case box1 empty box2 checked
    c = Consent(pdf_filepath=FilePath(pdf_file), omr_res=[res_empty, res_checked2])
    assert c.consent == box_id2

    # case box1 filled box2 checked
    c = Consent(pdf_filepath=FilePath(pdf_file), omr_res=[res_filled, res_checked2])
    assert c.consent == UNDERTERMINED
