import unittest

from src.extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_header_extraction(self):
        md = """
        # Hello
        """
        h1 = extract_title(md)
        self.assertEqual(h1, "Hello")

    def test_no_header(self):
        md = """
        there is no h1 header
        """
        with self.assertRaises(Exception):
            extract_title(md)

    def test_header_extra_spaces(self):
        md = """
        #    three extra spaces in header after #
        """
        h1 = extract_title(md)
        self.assertEqual(h1, "three extra spaces in header after #")

    def test_h1_header_and_other_headers(self):
        md = """
        ### h3 header here
        ## h2 header
        # and finally h1 header
        """
        h1 = extract_title(md)
        self.assertEqual(h1, "and finally h1 header")

    def test_multiple_h1_headers(self):
        md = """
        # first h1 header
        # second h1 header
        # third h1 header
        """
        h1 = extract_title(md)
        self.assertEqual(h1,"first h1 header")

    def test_no_space_after_hash(self):
        md = """
        #Hello
        """
        with self.assertRaises(Exception):
            extract_title(md)

    def test_header_with_leading_whitespaces(self):
        md = """
           #   Indented h1
        """
        h1 = extract_title(md)
        self.assertEqual(h1, "Indented h1")

    def test_header_not_at_the_start_of_the_document(self):
        md = """
        some text here
        and some more text
        # and the h1 header
        """
        h1 = extract_title(md)
        self.assertEqual(h1, "and the h1 header")

    def test_header_with_only_hash(self):
        md = """
        #
        """
        with self.assertRaises(Exception):
            extract_title(md)

    def test_werid_casing_or_unicode(self):
        md = """
        # Héllo 你好
        """
        h1 = extract_title(md)
        self.assertEqual(h1, "Héllo 你好")