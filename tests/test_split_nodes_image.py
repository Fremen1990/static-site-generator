import unittest

from src.splitters.split_nodes_image import split_nodes_image
from src.textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images_with_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        nodes_after_splitting = split_nodes_image([node])
        self.assertListEqual(        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        nodes_after_splitting,)

    def test_split_images_with_no_image(self):
        node = TextNode("This is text with no image", TextType.TEXT)
        nodes_after_splitting = split_nodes_image([node])
        self.assertListEqual([node], nodes_after_splitting)

    def test_split_images_with_single_image(self):
        node = TextNode("This is test with a single ![image](https://example.com/image.png)", TextType.TEXT)
        nodes_after_splitting = split_nodes_image([node])
        self.assertListEqual([
            TextNode("This is test with a single", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png")
        ], nodes_after_splitting)

    def test_split_images_with_empty_text(self):
        node = TextNode(
            "![image](https://example.com/image.png)",
            TextType.TEXT,
        )
        nodes_after_splitting = split_nodes_image([node])
        self.assertListEqual([
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ],
            nodes_after_splitting)

    def test_split_images_with_multiple_nodes(self):
        node1 = TextNode("Text with ![image1](https://example.com/1.png)", TextType.TEXT)
        node2 = TextNode("Another with ![image2](https://example.com/2.png)", TextType.TEXT)
        nodes_after_splitting = split_nodes_image([node1, node2])
        self.assertListEqual([
            TextNode("Text with ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "https://example.com/1.png"),
            TextNode("Another with ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/2.png"),
        ], nodes_after_splitting)

    def test_split_images_with_non_text_nodes(self):
        text_node = TextNode("Text with ![image](https://example.com/img.png)", TextType.TEXT)
        bold_node = TextNode("Bold text", TextType.BOLD)
        nodes_after_splitting = split_nodes_image([text_node, bold_node])
        self.assertListEqual([
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            bold_node,
        ], nodes_after_splitting)

    def test_split_images_at_beginning_and_end(self):
        node = TextNode("![start](https://example.com/start.png) middle ![end](https://example.com/end.png)",
                        TextType.TEXT)
        nodes_after_splitting = split_nodes_image([node])
        self.assertListEqual([
            TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
        ], nodes_after_splitting)