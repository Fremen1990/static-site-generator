import textwrap
import unittest

from src.markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block_with_no_blank_lines(self):
        md = """
        Single block of text with no blank lines
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,["Single block of text with no blank lines"])

    def test_leading_and_trailing_blank_lines(self):
        md = textwrap.dedent("""

        This is a middle of the text where before and after are empty blank lines

        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         [
                             "This is a middle of the text where before and after are empty blank lines",
                         ])

    def test_multiple_blank_lines_between_blocks(self):
        md = textwrap.dedent("""


        There are three blank lines before the text, and two blank lines after


        """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "There are three blank lines before the text, and two blank lines after"
        ])

    def test_empty_markdown_string(self):
        md = """"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


    def test_advanced_markdown_structure_to_blocks(self):
        md = textwrap.dedent("""
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """)
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_windows_line_endings(self):
        md = "First paragraph\r\n\r\nSecond paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_old_mac_line_endings(self):
        md = "First paragraph\r\rSecond paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_mixed_line_endings(self):
        md = "First paragraph\r\n\rSecond paragraph\n\nThird paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph", "Third paragraph"])

    def test_whitespace_only_lines(self):
        md = "First paragraph\n    \nSecond paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_multiple_whitespace_lines(self):
        md = "First paragraph\n  \n    \n\t\nSecond paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_complex_mixed_scenario(self):
        md = "First paragraph\r\n  \r\n\r    \nSecond paragraph\n\t\n\r\nThird paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph", "Third paragraph"])

    def test_whitespace_at_file_boundaries(self):
        md = "  \n\nFirst paragraph\n\n  \nSecond paragraph\n\t\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_tab_separated_blocks(self):
        md = "First paragraph\n\t\nSecond paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_many_consecutive_blank_lines(self):
        md = "First paragraph\n\n\n\n\n\nSecond paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])
