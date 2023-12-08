"""
Detect orientation of an image from a document
"""

__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@genomecad.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GLP3"
__version__= "1.0.0"

from typing import Literal
from pydantic import FilePath
from pytesseract import Output
import pytesseract
import imutils
import cv2


def image_2_Mat(file_path: FilePath) -> cv2.Mat:
    if file_path.exists:
        return cv2.imread(f"{file_path.resolve()}")
    else:
        return None


# def image_2_osd(img: FilePath, 
#                code: int = cv2.COLOR_BGR2RGB, 
#                output_type: Literal = Output.DICT):
#    return pytesseract.image_to_osd(cv2.cvtColor(cv2.imread(f"{img.resolve()}"), code), 
#                                    output_type=output_type)


def image_2_osd(img: cv2.Mat, 
                code: int = cv2.COLOR_BGR2RGB, 
                output_type: Literal = Output.DICT):
    return pytesseract.image_to_osd(cv2.cvtColor(img, code), output_type=output_type)


def rotate_image(img: cv2.Mat, rotation_angle: str, out_filepath: str):
    rotated_img = imutils.rotate_bound(img, angle=rotation_angle)
    cv2.imwrite(out_filepath, rotated_img)

if __name__ == "__main__":
    print(f"{__file__} package")
    print(__version__)
    print(__authors__)