from typing import List

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter:str, text_type: TextType)-> List[TextNode]:
    text_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            text_nodes.append(node)
            continue


        if delimiter not in node.text:
            text_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise Exception("unmatched delimiter")

        splits = node.text.split(delimiter)

        for index, element in enumerate(splits):
            if element == "":
                continue


            node_type = text_type if index % 2 == 1 else TextType.TEXT

            text_nodes.append(TextNode(element, node_type))

    return text_nodes


