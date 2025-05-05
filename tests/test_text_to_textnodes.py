import unittest

from src.text_to_textnodes import text_to_textnodes
from src.textnode import TextNode, TextType


class TestTextToTextnodes(unittest.TestCase):
    def test_convert_raw_text_to_textnodes(self):
        raw_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node_after_conversion = text_to_textnodes(raw_text)
        expected_node_after_conversion=[
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        self.assertListEqual(node_after_conversion, expected_node_after_conversion)

    def test_empty_string(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_plain_text(self):
        text = "Just plain text, no markdown"
        expected = [TextNode(text, TextType.TEXT)]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_bold_only(self):
        text = "**Bold text**"
        expected = [TextNode("Bold text", TextType.BOLD)]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_italic_only(self):
        text = "_Italic text_"
        expected = [TextNode("Italic text", TextType.ITALIC)]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_code_only(self):
        text = "`Code block`"
        expected = [TextNode("Code block", TextType.CODE)]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_image_only(self):
        text = "![alt text](https://example.com/image.jpg)"
        expected = [TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg")]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_link_only(self):
        text = "[link text](https://example.com)"
        expected = [TextNode("link text", TextType.LINK, "https://example.com")]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_adjacent_markdown(self):
        text = "**Bold**_Italic_`Code`"
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("Code", TextType.CODE)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_multiple_same_type(self):
        text = "**Bold1** plain text **Bold2**"
        expected = [
            TextNode("Bold1", TextType.BOLD),
            TextNode(" plain text ", TextType.TEXT),
            TextNode("Bold2", TextType.BOLD)
        ]
        self.assertListEqual(text_to_textnodes(text), expected)