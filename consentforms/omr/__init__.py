"""
Detect template of image
"""

__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@genomecad.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GLP3"
__version__ = "1.0.0"
__disclaimer__ = """
Based on simpleomr from https://github.com/EuracBiomedicalResearch/RescueOMR
# Copyright(c) 2016-2017: Yuri D'Elia <yuri.delia@eurac.edu>
# Copyright(c) 2016-2017: EURAC, Institute of Genetic Medicine

Thanks to the work of Yuri D'Elia
"""

from enum import IntEnum
import logging
import sys
import re
from typing import List, Optional

from PIL import Image, ImageDraw, ImageOps
import numpy as np
from pydantic import BaseModel
import scipy as sp
import lxml.etree

# tuned for 300 dpi grayscale text
BLACK_LEVEL = 0.80 * 255
OVRF_THR = 0.350
FILL_THR = 0.040
VOID_THR = 0.008

# H/V line rejection
CLEAN_LEN = 47  # window length (must be odd)
CLEAN_W = 3  # line width-1 (even)
CLEAN_THR = 0.9  # rejection threshold


class OmrTemplateError(Exception):
    """Exception raised for errors in template.

    Attributes:
        template -- template
        message -- explanation of the error
    """

    def __init__(self, template, message):
        self.template = template
        self.message = message
        super().__init__(f"Error on {self.template} template: {self.message}")


class OmrValueEnum(IntEnum):
    UNKNOWN = -1
    EMPTY = 0
    CHECKED = 1
    FILLED = 2


class OmrResult(BaseModel):
    template_search_area_id: str
    value: OmrValueEnum
    pixel_constituent: Optional[float]


def load_image(path: str):
    image = Image.open(path)
    image = image.convert('L')
    image = ImageOps.autocontrast(image)
    return np.array(image)


def _svg_translate(tag, tx=0, ty=0):
    if tag is None:
        return tx, ty
    trn = tag.get('transform')
    if trn is not None:
        grp = re.match(r'^translate\(([-\d.]+),([-\d.]+)\)$', trn)
        if grp is None:
            logging.error('SVG node contains unsupported transformations!')
            sys.exit(1)
        tx += float(grp.group(1))
        ty += float(grp.group(2))
    return _svg_translate(tag.getparent(), tx, ty)


def load_svg_rects(path, shape):
    data = lxml.etree.parse(path).getroot()
    dw = shape[1] / float(data.get('width'))
    dh = shape[0] / float(data.get('height'))
    rects = []
    for tag in data.iterfind('.//{*}rect'):
        tx, ty = _svg_translate(tag)
        i = tag.get('id')
        x = int((float(tag.get('x')) + tx) * dw)
        y = int((float(tag.get('y')) + ty) * dh)
        w = int(float(tag.get('width')) * dw)
        h = int(float(tag.get('height')) * dh)
        rects.append((i, x, y, w, h))
    return rects


def clean_image(image):
    s = CLEAN_LEN
    w = CLEAN_W
    k = -np.ones(shape=(s, s))
    k[:, s // 2 - w + 1:s // 2 + w] = 1
    k[s // 2 - w + 1:s // 2 + w, :] = 1
    tmp = sp.ndimage.convolve(image / 255, k) / np.sum(k)
    ret = image.copy()
    ret[tmp > CLEAN_THR] = 255
    return ret


def scan_marks(image, marks) -> List[OmrResult]:
    res = []
    for i, x, y, w, h in marks:
        roi = image[y:y + h, x:x + w]
        scr = (roi < BLACK_LEVEL).sum() / (w * h)
        if scr > OVRF_THR:
            v = OmrValueEnum.FILLED
        elif scr > FILL_THR:
            v = OmrValueEnum.CHECKED
        elif scr < VOID_THR:
            v = OmrValueEnum.EMPTY
        else:
            v = OmrValueEnum.UNKNOWN
        res.append(OmrResult(template_search_area_id=i, value=v, pixel_constituent=scr))
    return res


def debug_marks(path, image, clean, marks, res: List[OmrResult]):
    buf = Image.new('RGB', image.shape[::-1])
    buf.paste(Image.fromarray(image, 'L'))
    draw = ImageDraw.Draw(buf, 'RGBA')
    for mark, row in zip(marks, res):
        i, x, y, w, h = mark
        v = row.value
        if v == 1:
            c = (255, 0, 0, 127)
        elif v == 0:
            c = (0, 255, 0, 127)
        elif v == 2:
            c = (0, 0, 0, 64)
        else:
            c = (255, 127, 0, 127)
        draw.rectangle((x, y, x + w, y + h), c)
    bw = clean.copy()
    thr = bw < BLACK_LEVEL
    bw[thr] = 255
    bw[~thr] = 0
    buf.paste((0, 127, 255),
              (0, 0, image.shape[1], image.shape[0]),
              Image.fromarray(bw, 'L'))
    buf.save(path)


if __name__ == "__main__":
    print(f"{__file__} package")
    print(__version__)
    print(__authors__)

    print(__disclaimer__)
