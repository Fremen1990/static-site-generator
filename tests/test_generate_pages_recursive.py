import os
import shutil
import unittest

class TestGeneratePagesRecursive(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.test_content_dir = "test_content"
        self.test_public_dir = "test_public"
        self.template_path = "test_template.html"

        # Create directory structure
        os.makedirs(self.test_content_dir, exist_ok=True)
        os.makedirs(os.path.join(self.test_content_dir, "blog"), exist_ok=True)

        # Create a template file
        with open(self.template_path, "w", encoding="utf-8") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

        # Create some test markdown files
        with open(os.path.join(self.test_content_dir, "index.md"), "w", encoding="utf-8") as f:
            f.write("# Home Page\nWelcome to the test site.")

        with open(os.path.join(self.test_content_dir, "blog", "post1.md"), "w", encoding="utf-8") as f:
            f.write("# Test Post\nThis is a test post.")

        # Create a non-markdown file that should be ignored
        with open(os.path.join(self.test_content_dir, "ignore.txt"), "w", encoding="utf-8") as f:
            f.write("This file should be ignored")

    def tearDown(self):
        # Clean up test directories and files
        shutil.rmtree(self.test_content_dir, ignore_errors=True)
        shutil.rmtree(self.test_public_dir, ignore_errors=True)
        if os.path.exists(self.template_path):
            os.remove(self.template_path)

    def test_generate_pages_recursive(self):
        # Import your function here to avoid circular imports
        from src.generate_pages_recursive import generate_pages_recursive

        # Run the function being tested
        generate_pages_recursive(self.test_content_dir, self.template_path, self.test_public_dir)

        # Check if the expected HTML files exist
        self.assertTrue(os.path.exists(os.path.join(self.test_public_dir, "index.html")))
        self.assertTrue(os.path.exists(os.path.join(self.test_public_dir, "blog", "post1.html")))

        # Check that non-markdown files were not processed
        self.assertFalse(os.path.exists(os.path.join(self.test_public_dir, "ignore.html")))

        # Verify the content of generated files
        with open(os.path.join(self.test_public_dir, "index.html"), "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("<title>Home Page</title>", content)
            # Just check that the content appears somewhere in the HTML
            self.assertIn("Home Page", content)
            self.assertIn("Welcome to the test site", content)

        with open(os.path.join(self.test_public_dir, "blog", "post1.html"), "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("<title>Test Post</title>", content)
            self.assertIn("Test Post", content)
            self.assertIn("This is a test post", content)