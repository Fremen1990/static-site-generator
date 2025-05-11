import unittest



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
            TextNode("This is test with a single ", TextType.TEXT),
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

import unittest

from src.splitters.splitters import split_nodes_link, split_nodes_image
from src.textnode import TextNode, TextType

# @unittest.skip("Skipping TestSplitNodesLink for now")
class TestSplitNodesLink(unittest.TestCase):
    def test_split_links_with_multiple_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        nodes_after_splitting = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        nodes_after_splitting,)

    def test_split_links_with_no_link(self):
        node = TextNode("This is text with no link", TextType.TEXT)
        nodes_after_splitting = split_nodes_link([node])
        self.assertListEqual([node], nodes_after_splitting)

    def test_split_links_with_single_link(self):
        node = TextNode("This is test with a single [link](https://example.com/page.html)", TextType.TEXT)
        nodes_after_splitting = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is test with a single ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/page.html")
        ], nodes_after_splitting)

    def test_split_links_with_empty_text(self):
        node = TextNode(
            "[link](https://example.com/page.html)",
            TextType.TEXT,
        )
        nodes_after_splitting = split_nodes_link([node])
        self.assertListEqual([
            TextNode("link", TextType.LINK, "https://example.com/page.html"),
        ],
            nodes_after_splitting)

    def test_split_links_with_multiple_nodes(self):
        node1 = TextNode("Text with [link1](https://example.com/1.html)", TextType.TEXT)
        node2 = TextNode("Another with [link2](https://example.com/2.html)", TextType.TEXT)
        nodes_after_splitting = split_nodes_link([node1, node2])
        self.assertListEqual([
            TextNode("Text with ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com/1.html"),
            TextNode("Another with ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example.com/2.html"),
        ], nodes_after_splitting)

    def test_split_links_with_non_text_nodes(self):
        text_node = TextNode("Text with [link](https://example.com/page.html)", TextType.TEXT)
        bold_node = TextNode("Bold text", TextType.BOLD)
        nodes_after_splitting = split_nodes_link([text_node, bold_node])
        self.assertListEqual([
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com/page.html"),
            bold_node,
        ], nodes_after_splitting)

    def test_split_links_at_beginning_and_end(self):
        node = TextNode("[start](https://example.com/start.html) middle [end](https://example.com/end.html)",
                        TextType.TEXT)
        nodes_after_splitting = split_nodes_link([node])
        self.assertListEqual([
            TextNode("start", TextType.LINK, "https://example.com/start.html"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.LINK, "https://example.com/end.html"),
        ], nodes_after_splitting)