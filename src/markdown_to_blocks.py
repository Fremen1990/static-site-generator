from typing import List

def markdown_to_blocks(markdown: str)-> List[str]:
    result = []

    blocks = markdown.split("\n\n")

    for block in blocks:
        stripped_block = block.strip()

        if stripped_block != "":
            result.append(stripped_block)

    return result