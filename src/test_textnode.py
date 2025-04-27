import unittest
from unittest import TestCase

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


# @unittest.skip("Skipping this whole test class for now!")
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none_by_default(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_not_equal_different_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_urls(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK, "https://another-site.com")
        self.assertNotEqual(node, node2)

    def test_not_equal_one_with_url(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        node2 = TextNode("Link text", TextType.LINK)
        self.assertNotEqual(node, node2)


class TestHtmlNode(unittest.TestCase):
    def test_node_with_no_props(self):
        node = HTMLNode()
        node2 = "HTMLNode(tag=None, value=None, children=[], props={})"
        self.assertEqual(repr(node),node2)

    def test_properly_raise_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_with_attributes(self):
        node = HTMLNode(tag="a", props={"href": "https://boot.dev", "target": "_blank"})
        expected = ' href="https://boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_node_with_children(self):
        child = HTMLNode(tag="span", value="child")
        parent = HTMLNode(tag="div", children=[child])
        self.assertEqual(len(parent.children), 1)

    def test_node_with_multiple_children(self):
        child1 = HTMLNode(tag="li", value="List item 1")
        child2 = HTMLNode(tag="li", value="List item 2")
        parent = HTMLNode(tag="ul", children=[child1, child2])
        self.assertEqual(len(parent.children), 2)

    def test_node_with_both_value_and_children(self):
        child = HTMLNode(tag="b", value="bold")
        parent = HTMLNode(tag="p", value="Hello", children=[child])
        self.assertEqual(parent.value, "Hello")
        self.assertEqual(len(parent.children), 1)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold text.")
        self.assertEqual(node.to_html(), "<b>This is bold text.</b>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_img_with_props(self):
        node = LeafNode("img", "Image description", {"src": "image.jpg", "alt": "An example image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An example image">Image description</img>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text.")
        self.assertEqual(node.to_html(), "Just some text.")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()