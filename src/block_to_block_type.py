from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if not block or block.isspace():
        return BlockType.PARAGRAPH

    lines = block.split('\n')

    # Check for heading: starts with 1-6 # followed by space
    if lines[0].startswith('#'):
        # Extract potential heading marker
        parts = lines[0].split(' ', 1)
        if len(parts) > 1 and 1 <= len(parts[0]) <= 6 and all(char == '#' for char in parts[0]):
            return BlockType.HEADING

    # Check for code block: starts and ends with ```
    if block.startswith('```') and block.rstrip().endswith('```'):
        return BlockType.CODE

    # Check for quote: every line starts with >
    if all(line.startswith('>') for line in lines if line.strip()):
        return BlockType.QUOTE

    # Check for unordered list: every line starts with "- " (dash followed by space)
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list: every line starts with a number, dot, and space
    # Numbers must start at 1 and increment by 1 for each line
    is_ordered_list_format = True
    numbers = []

    for line in lines:
        parts = line.split('. ', 1)
        if len(parts) <= 1 or not parts[0].isdigit():
            is_ordered_list_format = False
            break
        numbers.append(int(parts[0]))

    if is_ordered_list_format:
        # For single-line lists
        if len(numbers) == 1:
            # A single-line ordered list must start with 1
            if numbers[0] != 1:
                return BlockType.PARAGRAPH
        else:  # Multi-line lists
            # Check if numbers are sequential (increment by 1)
            for i in range(1, len(numbers)):
                if numbers[i] != numbers[i - 1] + 1:
                    return BlockType.PARAGRAPH

        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH