from typing import List

from src.markdown_extraction import extract_markdown_links
from src.splitters.markdown_splitting import split_nodes_by_markdown
from src.textnode import TextNode, TextType


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_by_markdown(
        old_nodes,
        extract_markdown_links,
        TextType.LINK,
        prefix=""  # No prefix for links, unlike images which use "!"
    )