from typing import List

from src.splitters.split_nodes_bold import split_nodes_bold
from src.splitters.split_nodes_code import split_nodes_code
from src.splitters.split_nodes_image import split_nodes_image
from src.splitters.split_nodes_italic import split_nodes_italic
from src.splitters.split_nodes_link import split_nodes_link
from src.textnode import TextNode, TextType


def text_to_textnodes(text: str) -> List[TextNode]:
    if not text:
        return []


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
