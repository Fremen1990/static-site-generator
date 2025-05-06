import unittest

from src.block_to_block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    # Paragraph tests
    def test_simple_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph\nwith multiple lines"), BlockType.PARAGRAPH)

    def test_paragraph_with_special_chars(self):
        self.assertEqual(block_to_block_type("Paragraph with * # - > characters"), BlockType.PARAGRAPH)

    # Heading tests
    def test_h1_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)

    def test_h6_heading(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_invalid_heading_no_space(self):
        self.assertEqual(block_to_block_type("#Invalid heading"), BlockType.PARAGRAPH)

    def test_invalid_heading_too_many_hash(self):
        self.assertEqual(block_to_block_type("####### Too many #"), BlockType.PARAGRAPH)

    # Code block tests
    def test_simple_code_block(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)

    def test_multiline_code_block(self):
        self.assertEqual(block_to_block_type("```\nLine 1\nLine 2\nLine 3\n```"), BlockType.CODE)

    def test_invalid_code_block_unclosed(self):
        self.assertEqual(block_to_block_type("```\nUnclosed code block"), BlockType.PARAGRAPH)

    def test_invalid_code_block_inline(self):
        self.assertEqual(block_to_block_type("Not a ```code block```"), BlockType.PARAGRAPH)

    # Quote block tests
    def test_simple_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_multiline_quote_block(self):
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2\n> Line 3"), BlockType.QUOTE)

    def test_invalid_quote_block(self):
        self.assertEqual(block_to_block_type("> Line 1\nLine 2 without >"), BlockType.PARAGRAPH)

    # Unordered list tests
    def test_simple_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)

    def test_multiline_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)

    def test_invalid_unordered_list_no_space(self):
        self.assertEqual(block_to_block_type("-Invalid item"), BlockType.PARAGRAPH)

    def test_invalid_unordered_list_inconsistent(self):
        self.assertEqual(block_to_block_type("- Item 1\nItem 2 without -"), BlockType.PARAGRAPH)

    # Ordered list tests
    def test_simple_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)

    def test_multiline_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)

    def test_invalid_ordered_list_no_space(self):
        self.assertEqual(block_to_block_type("1.Invalid item"), BlockType.PARAGRAPH)

    def test_invalid_ordered_list_wrong_sequence(self):
        self.assertEqual(block_to_block_type("1. Item 1\n3. Item 3"), BlockType.PARAGRAPH)

    def test_invalid_ordered_list_not_starting_with_one(self):
        self.assertEqual(block_to_block_type("2. Item 2"), BlockType.PARAGRAPH)

    def test_invalid_ordered_list_inconsistent(self):
        self.assertEqual(block_to_block_type("1. Item 1\nItem 2 without number"), BlockType.PARAGRAPH)

    # Additional edge cases

    def test_empty_string(self):
        """Test that an empty string is treated as a paragraph."""
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_whitespace_only(self):
        """Test that whitespace-only blocks are treated as paragraphs."""
        self.assertEqual(block_to_block_type("   \n  \t  "), BlockType.PARAGRAPH)

    def test_heading_with_trailing_content(self):
        """Test a heading with content after it."""
        self.assertEqual(block_to_block_type("# Heading\nMore content"), BlockType.HEADING)

    def test_code_block_with_language_specifier(self):
        """Test a code block with a language specifier."""
        self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), BlockType.CODE)

    def test_quote_block_with_empty_lines(self):
        """Test a quote block with empty quoted lines."""
        self.assertEqual(block_to_block_type("> Line 1\n>\n> Line 3"), BlockType.QUOTE)

    def test_unordered_list_with_different_markers(self):
        """Test what happens if different markers are used."""
        self.assertEqual(block_to_block_type("- Item 1\n* Item 2"), BlockType.PARAGRAPH)

    def test_ordered_list_with_large_numbers(self):
        """Test ordered list with large numbers that follow proper sequence."""
        self.assertEqual(block_to_block_type(
            "1. Item 1\n2. Item 2\n3. Item 3\n4. Item 4\n5. Item 5\n6. Item 6\n7. Item 7\n8. Item 8\n9. Item 9\n10. Item 10"),
                         BlockType.ORDERED_LIST)

    def test_ordered_list_double_digit_sequence(self):
        """Test ordered list with double-digit numbers in sequence."""
        self.assertEqual(block_to_block_type("9. Item 9\n10. Item 10\n11. Item 11"), BlockType.ORDERED_LIST)

    def test_mixed_content_not_at_start_of_line(self):
        """Test that markdown syntax not at the start of a line doesn't change block type."""
        self.assertEqual(block_to_block_type("This line has a # in the middle"), BlockType.PARAGRAPH)

    def test_nested_markup_in_paragraph(self):
        """Test that nested markup in a paragraph doesn't change block type."""
        self.assertEqual(block_to_block_type("This paragraph has a\n> quote\nand a\n# heading\ninside"),
                         BlockType.PARAGRAPH)