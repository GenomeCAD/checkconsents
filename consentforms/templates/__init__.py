"""
Detect template of image
"""

__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@genomecad.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GNU AGLP3"
__version__ = "1.0.0"


import logging
from pathlib import Path
from typing import Dict
from pydantic import BaseModel, FilePath, conint
import pytesseract
from PIL import Image
from difflib import SequenceMatcher


LOGGER = logging.getLogger(__name__)

class FindTemplateError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Template(BaseModel):
    path: FilePath
    pattern: str
    priority: conint(gt=0)


def find_best_template(img: Path,
                       pages: Dict[str, str],
                       templates: Dict[str, Template],
                       parsing_header_limit: int = 5) -> str:
    found_line = False
    found_template = False
    best_match = {}
    best_template = None
    if img.exists():
        LOGGER.debug("debug best template")
        lines = pytesseract.image_to_string(Image.open(img.resolve())).splitlines()
        LOGGER.debug("ocr done")
        LOGGER.debug(pages)
        if not lines or len(lines) == 0:
            msg = f"ocr process does not return any lines, the image ({img.resolve()}) can't be processed to find a template. Skipping..."
            LOGGER.error(msg)
            raise FindTemplateError(msg)
        for i in range(min(len(lines), parsing_header_limit)):
            for key in pages:
                LOGGER.debug(pages[key])
                simil_score = SequenceMatcher(None, lines[i], pages[key]).ratio()
                if simil_score > 0.8:
                    found_line = True
                    break
        LOGGER.debug(f"found_line: {found_line}")
        if found_line:
            for i in range(min(len(lines), parsing_header_limit)):
                for key in templates:
                    simil_score = SequenceMatcher(None, lines[i], templates[key].pattern).ratio()
                    if simil_score > 0.90:
                        LOGGER.info(f"The following document is using template {key} with a confidence of {simil_score:.2f}")
                        best_match[key] = simil_score * templates[key].priority
                        found_template = True
        LOGGER.debug(f"found_template: {found_template}")
        if found_template:
            best_template_key = max(best_match, key=best_match.get)
            best_template = templates[best_template_key].path
    return best_template


if __name__ == "__main__":
    print(f"{__file__} package")
    print(__version__)
    print(__authors__)
