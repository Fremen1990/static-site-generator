from htmlnode import LeafNode
from textnode import TextNode, TextType


# from typing import Dict,Callable

# Nice and clean solution with `match` - but available from python v3.10
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid TextType: {text_node.text_type}")


# Cool solution with Dictionary map
# def text_node_to_html_node(text_node: TextNode) -> LeafNode:
#     converters: Dict[TextType, Callable[[], LeafNode]] = {
#         TextType.TEXT: lambda: LeafNode(None, text_node.text),
#         TextType.BOLD: lambda: LeafNode("b", text_node.text),
#         TextType.ITALIC: lambda: LeafNode("i", text_node.text),
#         TextType.CODE: lambda: LeafNode("code", text_node.text),
#         TextType.LINK: lambda: LeafNode("a", text_node.text, {"href": text_node.url}),
#         TextType.IMAGE: lambda: LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
#     }
#
#     converter = converters.get(text_node.text_type)
#
#     if converter is None:
#         raise ValueError(f"Invalid TextType: {text_node.text_type}")
#
#     return converter()

