import os

import cv2
from os import path

import numpy
from pydantic import FilePath

from consentforms import images as i
from tests.conftest import StepEnum, TEST_LOGGER

IMG_FILEPATH = FilePath(path.join(path.dirname(__file__), "resources/consentement-1-3.png"))
ROTATED_IMG_FILEPATH = FilePath(path.join(path.dirname(__file__), "resources/consentement-1-3_rotated.png"))


def test_image_2_mat():
    assert i.image_2_mat(None) is None
    img = i.image_2_mat(IMG_FILEPATH)
    assert img is not None
    assert numpy.array_equal(cv2.imread(str(IMG_FILEPATH.resolve())), img)


def test_image_file_2_osd():
    assert i.image_file_2_osd(IMG_FILEPATH) is not None


def test_image_2_osd():
    assert i.image_2_osd(i.image_2_mat(IMG_FILEPATH)) == i.image_file_2_osd(IMG_FILEPATH)


def test_rotate_image():
    img = i.image_2_mat(IMG_FILEPATH)
    rotated_img = i.rotate_image(img,
                                 90,
                                 str(ROTATED_IMG_FILEPATH))
    res_rotated_img = i.image_2_mat(ROTATED_IMG_FILEPATH.resolve())
    assert not numpy.array_equal(rotated_img, img)
    assert numpy.array_equal(rotated_img, res_rotated_img)
    os.remove(ROTATED_IMG_FILEPATH.resolve())


def test_convert_2_gray_scale():
    img = cv2.resize(i.image_2_mat(IMG_FILEPATH), (2480,3508), interpolation= cv2.INTER_LINEAR)
    assert numpy.array_equal(i.convert_2_gray_scale(img), cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))


def test_generate_crop_image(tmp_path, rotate_img_files):
    img_mat = i.image_2_mat(rotate_img_files.files.get(StepEnum.ROTATED).path)
    cropped_img_filepath = path.join(tmp_path, "cropped.png")
    assert i.generate_crop_image(img_mat, cropped_img_filepath)
    crop_img_mat = i.compute_crop_image(img_mat)
    res_img_mat = i.image_2_mat(FilePath(cropped_img_filepath))
    assert not numpy.array_equal(img_mat, crop_img_mat)
    assert numpy.array_equal(crop_img_mat, res_img_mat)


def test_sort_cnts_without_changing_crop_image(tmp_path, rotate_img_files):
    img_mat = i.image_2_mat(rotate_img_files.files.get(StepEnum.ROTATED).path)

    cnts = i.delimit_area(img_mat)
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])
    crop_img_mat_sorted = i.crop_image(img_mat, cnts)
    cv2.imwrite(path.join(tmp_path, "cropped-sorted.png"), crop_img_mat_sorted)

    cropped_img_filepath = path.join(tmp_path, "cropped.png")
    assert i.generate_crop_image(img_mat, cropped_img_filepath)
    crop_img_mat = i.image_2_mat(FilePath(cropped_img_filepath))

    assert numpy.array_equal(crop_img_mat, crop_img_mat_sorted)
