import re
from typing import List

def markdown_to_blocks(markdown: str)-> List[str]:
    normalized_markdown = markdown.replace('\r\n', '\n').replace('\r', '\n')

    blocks = re.split(r'\n\s*\n+', normalized_markdown)

    result = [block.strip() for block in blocks if block.strip()]

    return result