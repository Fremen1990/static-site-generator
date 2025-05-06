from enum import Enum
from typing import List


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    """Determine the type of markdown block."""
    if not block or block.isspace():
        return BlockType.PARAGRAPH

    lines = block.split('\n')

    # Use dedicated functions for each block type check
    if is_heading(lines):
        return BlockType.HEADING

    if is_code_block(block):
        return BlockType.CODE

    if is_quote(lines):
        return BlockType.QUOTE

    if is_unordered_list(lines):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def is_heading(lines: List[str]) -> bool:
    """Check if block is a heading."""
    if not lines[0].startswith('#'):
        return False

    parts = lines[0].split(' ', 1)
    return (len(parts) > 1 and
            1 <= len(parts[0]) <= 6 and
            all(char == '#' for char in parts[0]))


def is_code_block(block: str) -> bool:
    """Check if block is a code block."""
    return block.startswith('```') and block.rstrip().endswith('```')


def is_quote(lines: List[str]) -> bool:
    """Check if block is a quote."""
    return all(line.startswith('>') for line in lines if line.strip())


def is_unordered_list(lines: List[str]) -> bool:
    """Check if block is an unordered list."""
    return all(line.startswith('- ') for line in lines if line.strip())


def is_ordered_list(lines: List[str]) -> bool:
    """Check if block is an ordered list."""
    numbers = []

    # Check if every line starts with a number, dot, and space
    for line in lines:
        if not line.strip():  # Skip empty lines
            continue

        parts = line.split('. ', 1)
        if len(parts) <= 1 or not parts[0].isdigit():
            return False
        numbers.append(int(parts[0]))

    # Edge case: no valid numbered lines found
    if not numbers:
        return False

    # Check if numbers increment by 1 (regardless of starting number)
    for i in range(1, len(numbers)):
        if numbers[i] != numbers[i - 1] + 1:
            return False

    # Only require the first number to be 1 for single-line lists
    if len(numbers) == 1 and numbers[0] != 1:
        return False

    return True