from typing import List

from src.markdown_extraction import extract_markdown_images, extract_markdown_links
from src.splitters.markdown_splitting import split_nodes_by_markdown
from src.splitters.split_nodes_delimiter import split_nodes_delimiter
from src.textnode import TextNode, TextType


def split_nodes_bold(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_delimiter(old_nodes, "**", TextType.BOLD)


def split_nodes_code(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_delimiter(old_nodes, "`", TextType.CODE)


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_by_markdown(
        old_nodes,
        extract_markdown_images,
        TextType.IMAGE,
        prefix="!"
    )


def split_nodes_italic(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_by_markdown(
        old_nodes,
        extract_markdown_links,
        TextType.LINK,
        prefix=""  # No prefix for links, unlike images which use "!"
    )
