"""

"""

__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@genomecad.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GNU AGLP3"
__version__ = "1.0.0"


import cv2
import imutils
import logging
import pytesseract
from cv2 import Mat
from numpy import ndarray, dtype, generic
from os import system, popen, path
from pydantic import DirectoryPath, FilePath
from pytesseract import Output
from typing import Any


CONVERT_PAGE_SEPARATOR = "-"
CONVERT_PNG_EXT = ".png"


class PdfConvertError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def default_convert_output_format(root_filename: str,
                                  page_separator: str = CONVERT_PAGE_SEPARATOR,
                                  extension: str = CONVERT_PNG_EXT):
    return f"{root_filename}{page_separator}%d{extension}"


def convert_pdf_2_png(pdf_filepath: FilePath,
                      png_output_dir: DirectoryPath,
                      output_format: str,
                      density: int = 300,
                      optional_args: str = None):
    tool = "convert"
    #output_format = f"{pdf_filepath.stem}{CONVERT_PAGE_SEPARATOR}%d{CONVERT_PNG_EXT}"
    convert_output_filepath = path.join(png_output_dir.resolve(), output_format)
    cmd_args = f"-density {density} {pdf_filepath.resolve()} {convert_output_filepath}"
    cmd = [tool, cmd_args]
    if optional_args is not None:
        cmd.insert(1, optional_args)
    exec_cmd = ' '.join(cmd)
    exit_code = system(exec_cmd)
    if exit_code != 0:
        raise PdfConvertError(f"Conversion of {pdf_filepath.resolve()} failed, command: {exec_cmd}")
    return exit_code
    # stream = os.popen(f"convert -density {density} {pdf_filepath.resolve()} {png_filepath.resolve()}")
    # return stream.read()


def image_2_mat(file_path: FilePath) -> Mat | ndarray | ndarray[Any, dtype[generic | generic]] | None:
    if file_path is not None and file_path.exists():
        return cv2.imread(f"{file_path.resolve()}")
    else:
        return None


def image_file_2_osd(img: FilePath,
                     code: int = cv2.COLOR_BGR2RGB,
                     output_type: str = Output.DICT):
    return pytesseract.image_to_osd(cv2.cvtColor(cv2.imread(f"{img.resolve()}"), code),
                                    output_type=output_type)


def image_2_osd(img: cv2.Mat,
                code: int = cv2.COLOR_BGR2RGB,
                output_type: str = Output.DICT):
    return pytesseract.image_to_osd(cv2.cvtColor(img, code), output_type=output_type)


def rotate_image(img: cv2.Mat, rotation_angle: int, out_filepath: str) -> Mat | ndarray[Any, dtype[generic]] | ndarray:
    rotated_img = imutils.rotate_bound(img, angle=rotation_angle)
    cv2.imwrite(out_filepath, rotated_img)
    return rotated_img


def convert_2_gray_scale(img: cv2.Mat) -> cv2.Mat:
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def delimit_area(img: cv2.Mat):
    gray = convert_2_gray_scale(img)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    # blur = cv2.GaussianBlur(gray, (21, 21), 0) #Initial values
    # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] #Initial values
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))  # 3, 13
    # kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13)) #Initial values
    dilate = cv2.dilate(thresh, kernal, iterations=1)
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])
    return cnts


def crop_image(img: cv2.Mat, cnts) -> cv2.Mat:
    minx = 100000000
    miny = 100000000
    maxx = 0
    maxy = 0
    overall_width = 0
    overall_height = 0
    boxx = boxy = 0
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if x < minx:
            minx = x
        if y < miny:
            miny = y
        if x > maxx:
            maxx = x
            boxx = x + w
        if y > maxy:
            maxy = y
            boxy = h
        if w > overall_width:
            overall_width = w
    logging.debug(f"{miny}:{maxy + boxy}, {minx}:{minx + overall_width}")
    return img[miny:maxy + boxy, minx:minx + overall_width]


def generate_crop_image(img: cv2.Mat, out_filepath: str) -> bool:
    cropped_image = compute_crop_image(img)
    return cv2.imwrite(out_filepath, cropped_image)


def compute_crop_image(img: cv2.Mat) -> cv2.Mat:
    return crop_image(img, delimit_area(img))


if __name__ == "__main__":
    print(f"{__file__} package")
    print(__version__)
    print(__authors__)
