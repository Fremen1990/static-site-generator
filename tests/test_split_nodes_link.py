import unittest

from src.splitters.split_nodes_link import split_nodes_link
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