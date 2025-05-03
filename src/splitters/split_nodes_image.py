from typing import List

from src.markdown_extraction import extract_markdown_images
from src.textnode import TextNode, TextType


def split_nodes_image(old_nodes: List[TextNode])-> List[TextNode]:
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            result.append(old_node)
            continue

        current_text = old_node.text
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"

            parts = current_text.split(image_markdown, 1)

            if parts[0]:
                result.append(TextNode(parts[0], TextType.TEXT))

            result.append(TextNode(image_alt, TextType.IMAGE, image_url))

            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))

    return result