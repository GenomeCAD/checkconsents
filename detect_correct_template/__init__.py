"""
Detect template of image
"""

__authors__ = ("David Salgado", "Adrien Josso Rigonato")
__contact__ = ("david.salgado@genomecad.fr", "adrien.josso-rigonato@genomecad.fr")
__copyright__ = "GLP3"
__version__= "1.0.0"


import logging
from pathlib import Path
from typing import Dict
from pydantic import BaseModel, FilePath, conint
import pytesseract
from PIL import Image
from difflib import SequenceMatcher


LOGGER = logging.getLogger(__name__)


class Template(BaseModel):
    path: FilePath
    pattern: str
    priority: conint(gt=0)


def find_best_template(img: Path, pages: Dict[str, str], templates: Dict[str, Template], parsing_header_limit: int = 5) -> str:
    found_line = False
    found_template = False
    bestmatch = {}
    best_template = None
    if img.exists():
        LOGGER.debug("debug best template")
        lines = pytesseract.image_to_string(Image.open(img.resolve())).splitlines()
        LOGGER.debug("ocr done")
        LOGGER.debug(pages)
        for i in range(parsing_header_limit): 
            for key in pages:
                LOGGER.debug(pages[key])
                simil_score = SequenceMatcher(None, lines[i], pages[key]).ratio()
                if simil_score > 0.8:
                    found_line = True
                    break
        LOGGER.debug(f"found_line: {found_line}")
        if found_line == True:
            for i in range(parsing_header_limit):
                for key in templates:
                    simil_score = SequenceMatcher(None, lines[i], templates[key].pattern).ratio()
                    if simil_score > 0.90:
                            LOGGER.info(f"The following document is using template {key} with a confidence of {simil_score:.2f}")
                            bestmatch[key] = simil_score * templates[key].priority
                            found_template = True
        LOGGER.debug(f"found_template: {found_template}")
        if found_template == True :
            best_template_key = max(bestmatch, key=bestmatch.get)
            # if "tiers_apparente" in bestmatch :             #TODO explain the case and refactor to extract string value in constant/config : utiliser le niveau de priorité
            #     best_template_key = "tiers_apparente"
            best_template = templates[best_template_key].path
    return best_template


if __name__ == "__main__":
    print(f"{__file__} package")
    print(__version__)
    print(__authors__)
