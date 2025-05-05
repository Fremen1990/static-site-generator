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
        md = """

        This is a middle of the text where before and after are empty blank lines

        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         [
                             "This is a middle of the text where before and after are empty blank lines",
                         ])

    def test_multiple_blank_lines_between_blocks(self):
        md = """


        There are three blank lines before the text, and two blank lines after


        """
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

