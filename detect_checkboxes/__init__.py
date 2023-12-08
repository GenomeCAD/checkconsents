"""
Detect checkboxes into an image
"""

__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@genomecad.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GLP3"
__version__= "1.0.0"


import sys
import cv2
import numpy as np
from pydantic import FilePath


def image_2_Mat(file_path: FilePath) -> cv2.Mat:
    if file_path.exists:
        return cv2.imread(f"{file_path.resolve()}")
    else:
        return None 

def convert_2_gray_scale(img: cv2.Mat) -> cv2.Mat:
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def delimit_area(img: cv2.Mat):
    gray = convert_2_gray_scale(img)
    # blur = cv2.GaussianBlur(gray, (9,9), 0)
    blur = cv2.GaussianBlur(gray, (21,21), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU )[1]
    #thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
    #kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9)) #3,13
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,13))

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
    overallwidth = 0
    overallheight = 0
    boxx = boxy = 0
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if x < minx : 
            minx = x
        if y < miny : 
            miny = y
        if x > maxx :
            maxx = x
            boxx=x+w
        if y > maxy :
            maxy = y
            boxy = h
        if w > overallwidth :
            overallwidth = w
    return img[miny:maxy+boxy, minx:minx+overallwidth]


def generate_crop_image(img: cv2.Mat, out_filepath: str) -> bool:
    cropped_image = crop_image(img, delimit_area(img))
    return cv2.imwrite(out_filepath, cropped_image)


def compute_crop_image(img: cv2.Mat) -> cv2.Mat:
    return crop_image(img, delimit_area(img))
    

if __name__ == "__main__":
    print(f"{__file__} package")
    print(__version__)
    print(__authors__)
