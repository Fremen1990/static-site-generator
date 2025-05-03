import re
from typing import Tuple, List

from src.patterns import MARKDOWN_IMAGE_PATTERN, MARKDOWN_LINK_PATTERN


def extract_markdown_images(text:str)-> List[Tuple[str,str]]:
    matches = re.findall(MARKDOWN_IMAGE_PATTERN, text)
    return matches

def extract_markdown_links(text:str)-> List[Tuple[str, str]]:
    matches = re.findall(MARKDOWN_LINK_PATTERN, text)
    return matches