from typing import List, Tuple, Callable

from textnode import TextNode, TextType


def split_nodes_by_markdown(
    old_nodes: List[TextNode],
    extract_function: Callable[[str], List[Tuple[str, str]]],
    text_type: TextType,
    prefix: str = ""
) -> List[TextNode]:
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        items = extract_function(old_node.text)
        if not items:
            result.append(old_node)
            continue

        current_text = old_node.text
        for item_text, item_url in items:
            markdown = f"{prefix}[{item_text}]({item_url})"

            parts = current_text.split(markdown, 1)

            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(item_text, text_type, item_url))

            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    return result