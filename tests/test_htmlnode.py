import unittest

from src.htmlnode import HTMLNode, ParentNode, LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_node_with_no_props(self):
        node = HTMLNode()
        node2 = "HTMLNode(tag=None, value=None, children=[], props={})"
        self.assertEqual(repr(node), node2)

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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "test")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(parent_node.to_html(), '<div class="container" id="main"><span>child</span></div>')

    def test_to_html_with_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_none_children_after_init(self):
        parent_node = ParentNode("div", [])
        parent_node.children = None
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_mixed_children(self):
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode(None, "Plain")
        parent1 = ParentNode("span", [leaf1])
        parent_node = ParentNode("div", [leaf2, parent1])
        self.assertEqual(parent_node.to_html(), "<div>Plain<span><b>Bold</b></span></div>")
