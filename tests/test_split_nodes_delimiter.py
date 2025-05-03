import unittest

from src.splitters.split_nodes_delimiter import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_delimiter_splitting(self):
        raw_markdown_string = "This is text with a **bolded phrase** in the middle"
        starting_nodes = [TextNode(raw_markdown_string, TextType.TEXT)]
        text_nodes_list_after_splitting = split_nodes_delimiter(starting_nodes, "**", TextType.BOLD)
        expected_text_nodes_list_after_splitting = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT)
        ]
        self.assertEqual(text_nodes_list_after_splitting, expected_text_nodes_list_after_splitting)

    def test_double_bold_delimiter_splitting(self):
        starting_nodes = [
            TextNode("Normal text ", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode(" more **bold** here", TextType.TEXT),
        ]
        text_nodes_list_after_splitting = split_nodes_delimiter(starting_nodes, "**", TextType.BOLD)
        expected_text_nodes_list_after_splitting = [
            TextNode("Normal text ", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode(" more ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" here", TextType.TEXT)
            ]
        self.assertEqual(text_nodes_list_after_splitting, expected_text_nodes_list_after_splitting)

    def test_no_delimiter_present(self):
        starting_nodes =  [TextNode("Just normal text", TextType.TEXT)]
        text_nodes_list_after_splitting = split_nodes_delimiter(starting_nodes, "**", TextType.BOLD)
        expected_text_nodes_list_after_splitting = [TextNode("Just normal text", TextType.TEXT)]
        self.assertEqual(text_nodes_list_after_splitting, expected_text_nodes_list_after_splitting)

    def test_unclosed_delimiter(self):
        starting_nodes = [TextNode("Text with **bold but not end", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(starting_nodes, "**", TextType.BOLD)


    def test_multiple_delimiter_pairs(self):
        starting_nodes = [TextNode("Text with **first** and **second** bold", TextType.TEXT)]
        text_nodes_list_after_splitting = split_nodes_delimiter(starting_nodes, "**", TextType.BOLD)
        expected_text_nodes_list_after_splitting = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("first", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold", TextType.TEXT)
            ]
        self.assertEqual(text_nodes_list_after_splitting, expected_text_nodes_list_after_splitting)
