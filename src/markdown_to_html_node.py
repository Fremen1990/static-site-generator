from src.block_to_block_type import block_to_block_type, BlockType
from src.htmlnode import HTMLNode, ParentNode, LeafNode
from src.markdown_to_blocks import markdown_to_blocks
from src.text_to_textnodes import text_to_textnodes
from src.text_node_to_html_node import text_node_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        paragraph_text = ' '.join([line.strip() for line in block.split('\n')])
        return ParentNode("p", text_to_children(paragraph_text))

    elif block_type == BlockType.HEADING:
        # Extract heading level (number of #)
        level = 0
        for char in block:
            if char == '#':
                level += 1
            else:
                break

        # Get the heading text (removing the # prefix)
        heading_text = block[level:].strip()

        return ParentNode(f"h{level}", text_to_children(heading_text))

    elif block_type == BlockType.CODE:
        # Remove the ``` from start and end
        lines = block.split('\n')
        # Only keep content between the triple backticks and ensure proper newlines
        code_lines = lines[1:-1] if len(lines) > 2 else []
        # Make sure we preserve the newlines at the end of each line
        # Add an extra newline at the end to match the expected output
        code_content = '\n'.join(code_lines) + '\n'

        # Code blocks should not process inline markdown
        code_node = LeafNode("code", code_content)
        return ParentNode("pre", [code_node])

    elif block_type == BlockType.QUOTE:
        # Remove the > prefix from each line and join with space
        quote_lines = []
        for line in block.split('\n'):
            if line.strip():
                # Remove the '>' prefix and any leading space after it
                line_content = line.lstrip('>').lstrip()
                quote_lines.append(line_content)

        quote_content = ' '.join(quote_lines)
        return ParentNode("blockquote", text_to_children(quote_content))

    elif block_type == BlockType.UNORDERED_LIST:
        # Split into list items and remove the - prefix
        items = block.split('\n')
        list_items = []

        for item in items:
            if item.strip():
                item_text = item[2:].strip()  # Remove "- " prefix
                list_items.append(ParentNode("li", text_to_children(item_text)))

        return ParentNode("ul", list_items)

    elif block_type == BlockType.ORDERED_LIST:
        # Split into list items and remove the number prefix
        items = block.split('\n')
        list_items = []

        for item in items:
            if item.strip():
                # Find the position after the digit and dot
                parts = item.split('. ', 1)
                if len(parts) > 1:
                    item_text = parts[1].strip()
                    list_items.append(ParentNode("li", text_to_children(item_text)))

        return ParentNode("ol", list_items)

    # Default case (should not happen with proper block typing)
    return ParentNode("div", text_to_children(block))


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    html_nodes = [block_to_html_node(block) for block in blocks]

    return ParentNode("div", html_nodes)