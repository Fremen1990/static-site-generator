from typing import List, Callable, Dict, Optional
from block_to_block_type import block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_to_blocks import markdown_to_blocks
from text_to_textnodes import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node

# TODO: separate this to constants.py and reuse in all places in the app where we use these strings
# Constants for markdown syntax elements
HEADING_MARKER = '#'
CODE_FENCE = '```'
QUOTE_MARKER = '>'
UNORDERED_LIST_MARKER = '-'
NEWLINE = '\n'
SPACE = ' '


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", html_nodes)


def text_to_children(text: str) -> List[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)

    # Dictionary mapping block types to their handler functions
    block_handlers: Dict[BlockType, Callable[[str], HTMLNode]] = {
        BlockType.PARAGRAPH: _handle_paragraph_block,
        BlockType.HEADING: _handle_heading_block,
        BlockType.CODE: _handle_code_block,
        BlockType.QUOTE: _handle_quote_block,
        BlockType.UNORDERED_LIST: _handle_unordered_list_block,
        BlockType.ORDERED_LIST: _handle_ordered_list_block
    }

    handler = block_handlers.get(block_type)
    if handler:
        return handler(block)

    return ParentNode("div", text_to_children(block))


def _normalize_text_lines(block: str) -> str:
    lines = [line.strip() for line in block.split(NEWLINE)]
    return SPACE.join(line for line in lines if line)


def _handle_paragraph_block(block: str) -> HTMLNode:
    paragraph_text = _normalize_text_lines(block)
    return ParentNode("p", text_to_children(paragraph_text))


def _count_leading_characters(text: str, char: str) -> int:
    count = 0
    for c in text:
        if c == char:
            count += 1
        else:
            break
    return count


def _handle_heading_block(block: str) -> HTMLNode:
    level = _count_leading_characters(block, HEADING_MARKER)
    heading_text = block[level:].strip()
    return ParentNode(f"h{level}", text_to_children(heading_text))


def _extract_content_between_fences(block: str) -> str:
    lines = block.split(NEWLINE)

    # Skip first and last lines (the fences)
    content_lines = lines[1:-1] if len(lines) > 2 else []

    # Add trailing newline to match expected output
    return NEWLINE.join(content_lines) + NEWLINE


def _handle_code_block(block: str) -> HTMLNode:
    code_content = _extract_content_between_fences(block)
    code_node = LeafNode("code", code_content)
    return ParentNode("pre", [code_node])


def _remove_prefix_from_line(line: str, prefix: str) -> str:
    return line.lstrip(prefix).lstrip()


def _extract_quote_lines(block: str) -> List[str]:
    quote_lines = []
    for line in block.split(NEWLINE):
        if line.strip():
            line_content = _remove_prefix_from_line(line, QUOTE_MARKER)
            quote_lines.append(line_content)
    return quote_lines


def _handle_quote_block(block: str) -> HTMLNode:
    quote_lines = _extract_quote_lines(block)
    quote_content = SPACE.join(quote_lines)
    return ParentNode("blockquote", text_to_children(quote_content))


def _create_list_item(item_text: str) -> HTMLNode:
    return ParentNode("li", text_to_children(item_text))


def _extract_list_items(block: str, process_line: Callable[[str], Optional[str]]) -> List[HTMLNode]:
    list_items = []

    for line in block.split(NEWLINE):
        if not line.strip():
            continue

        item_text = process_line(line)
        if item_text:
            list_items.append(_create_list_item(item_text))

    return list_items


def _process_unordered_list_item(line: str) -> str:
    return _remove_prefix_from_line(line, UNORDERED_LIST_MARKER)


def _handle_unordered_list_block(block: str) -> HTMLNode:
    list_items = _extract_list_items(block, _process_unordered_list_item)
    return ParentNode("ul", list_items)


def _process_ordered_list_item(line: str) -> Optional[str]:
    # Find the first dot after a number
    dot_pos = line.find('.')
    if dot_pos > 0 and line[:dot_pos].strip().isdigit():
        return line[dot_pos + 1:].lstrip()
    return None


def _handle_ordered_list_block(block: str) -> HTMLNode:
    list_items = _extract_list_items(block, _process_ordered_list_item)
    return ParentNode("ol", list_items)