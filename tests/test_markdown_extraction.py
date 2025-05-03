import unittest

from src.markdown_extraction import extract_markdown_images, extract_markdown_links


class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links("This is text with a [link](https://www.example.com)")
        self.assertListEqual([("link", "https://www.example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)

    def test_extract_links_vs_images(self):
        text = "This has a link [link](https://example.com) and an ![image](https://example.com/img.jpg)"
        links = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], links)

        images = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.jpg")], images)

    def test_complex_urls(self):
        text = "[Complex link](https://example.com/path?param=value&other=stuff)"
        expected = [("Complex link", "https://example.com/path?param=value&other=stuff")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![  ](https://example.com/pic.png)")
        self.assertListEqual([("  ", "https://example.com/pic.png")], matches)