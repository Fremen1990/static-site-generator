from typing import List

from src.splitters.splitters import split_nodes_bold, split_nodes_italic, split_nodes_image, split_nodes_code, \
    split_nodes_link
from src.textnode import TextNode, TextType


def text_to_textnodes(text: str) -> List[TextNode]:
    if not text:
        return []

    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_bold(nodes)
    nodes = split_nodes_italic(nodes)
    nodes = split_nodes_code(nodes)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
