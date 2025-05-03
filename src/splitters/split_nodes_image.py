from typing import List

from src.markdown_extraction import extract_markdown_images
from src.splitters.markdown_splitting import split_nodes_by_markdown
from src.textnode import TextNode, TextType


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_by_markdown(
        old_nodes,
        extract_markdown_images,
        TextType.IMAGE,
        prefix="!"
    )
