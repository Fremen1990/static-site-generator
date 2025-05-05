from typing import List

from src.splitters.split_nodes_delimiter import split_nodes_delimiter
from src.textnode import TextNode, TextType


def split_nodes_bold(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

