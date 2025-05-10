import unittest
import os
import tempfile
from src.main import generate_public


class TestGeneratePublic(unittest.TestCase):
    def test_generate_public(self):
        # Set up temporary directories for source and destination
        with tempfile.TemporaryDirectory() as test_src, tempfile.TemporaryDirectory() as test_dst:
            # Create test file structure in the source directory
            # First level files
            with open(os.path.join(test_src, "file1.txt"), "w") as f:
                f.write("This is file 1")
            with open(os.path.join(test_src, "file2.txt"), "w") as f:
                f.write("This is file 2")

            # Create a subdirectory with files
            sub_dir = os.path.join(test_src, "subdir")
            os.makedirs(sub_dir)
            with open(os.path.join(sub_dir, "subfile1.txt"), "w") as f:
                f.write("This is subfile 1")

            # Create a nested subdirectory
            nested_dir = os.path.join(sub_dir, "nested")
            os.makedirs(nested_dir)
            with open(os.path.join(nested_dir, "nestedfile1.txt"), "w") as f:
                f.write("This is nested file 1")

            # Call the function being tested, passing our test directories
            generate_public(test_src, test_dst)

            # Verify the results

            # Check that all files exist in destination
            self.assertTrue(os.path.exists(os.path.join(test_dst, "file1.txt")))
            self.assertTrue(os.path.exists(os.path.join(test_dst, "file2.txt")))
            self.assertTrue(os.path.exists(os.path.join(test_dst, "subdir", "subfile1.txt")))
            self.assertTrue(os.path.exists(os.path.join(test_dst, "subdir", "nested", "nestedfile1.txt")))

            # Verify file contents
            with open(os.path.join(test_dst, "file1.txt"), "r") as f:
                self.assertEqual(f.read(), "This is file 1")

            with open(os.path.join(test_dst, "subdir", "nested", "nestedfile1.txt"), "r") as f:
                self.assertEqual(f.read(), "This is nested file 1")

    def test_generate_public_with_existing_destination(self):
        # Test that function properly cleans up existing destination
        with tempfile.TemporaryDirectory() as test_src, tempfile.TemporaryDirectory() as test_dst:
            # Create source files
            with open(os.path.join(test_src, "file1.txt"), "w") as f:
                f.write("This is file 1")

            # Create pre-existing file in destination that should be removed
            with open(os.path.join(test_dst, "old_file.txt"), "w") as f:
                f.write("This should be removed")

            # Call function
            generate_public(test_src, test_dst)

            # Verify old file was removed
            self.assertFalse(os.path.exists(os.path.join(test_dst, "old_file.txt")))

            # Verify new file exists
            self.assertTrue(os.path.exists(os.path.join(test_dst, "file1.txt")))

    def test_generate_public_no_source(self):
        # Test error handling when source doesn't exist
        with tempfile.TemporaryDirectory() as test_dst:
            non_existent_src = "/path/that/does/not/exist"

            # Function should raise an exception
            with self.assertRaises(Exception):
                generate_public(non_existent_src, test_dst)


if __name__ == "__main__":
    unittest.main()