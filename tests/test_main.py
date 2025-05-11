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

    def test_generate_public_empty_source(self):
        with tempfile.TemporaryDirectory() as test_src, tempfile.TemporaryDirectory() as test_dst:
            # Call function with empty source directory
            generate_public(test_src, test_dst)

            # Verify destination exists but is empty
            self.assertTrue(os.path.exists(test_dst))
            self.assertEqual(len(os.listdir(test_dst)), 0)

    def test_generate_public_special_characters(self):
        with tempfile.TemporaryDirectory() as test_src, tempfile.TemporaryDirectory() as test_dst:
            # Create file with special characters in name
            with open(os.path.join(test_src, "file with spaces.txt"), "w") as f:
                f.write("Content")

            # Create directory with special characters
            special_dir = os.path.join(test_src, "special_dir!")
            os.makedirs(special_dir)
            with open(os.path.join(special_dir, "子file.txt"), "w") as f:
                f.write("Unicode content")

            # Call function
            generate_public(test_src, test_dst)

            # Verify files were copied correctly
            self.assertTrue(os.path.exists(os.path.join(test_dst, "file with spaces.txt")))
            self.assertTrue(os.path.exists(os.path.join(test_dst, "special_dir!", "子file.txt")))

    def test_generate_public_with_symlinks(self):
        with tempfile.TemporaryDirectory() as test_src, tempfile.TemporaryDirectory() as test_dst:
            # Create a file and a symlink to it
            with open(os.path.join(test_src, "original.txt"), "w") as f:
                f.write("Original content")

            # Create symlink
            os.symlink(
                os.path.join(test_src, "original.txt"),
                os.path.join(test_src, "link.txt")
            )

            # Call function
            generate_public(test_src, test_dst)

            # Check if both original and link are in destination
            self.assertTrue(os.path.exists(os.path.join(test_dst, "original.txt")))

            # Depending on your implementation, the symlink might be copied as a regular file
            # or as a symlink. Adjust this test according to expected behavior.
            self.assertTrue(os.path.exists(os.path.join(test_dst, "link.txt")))

    def test_generate_public_large_file(self):
        with tempfile.TemporaryDirectory() as test_src, tempfile.TemporaryDirectory() as test_dst:
            # Create a relatively large file (e.g., 1 MB)
            large_file_path = os.path.join(test_src, "large_file.bin")
            with open(large_file_path, "wb") as f:
                f.write(b"0" * 1024 * 1024)  # 1 MB of zeros

            # Get file size for verification
            original_size = os.path.getsize(large_file_path)

            # Call function
            generate_public(test_src, test_dst)

            # Verify file was copied and size matches
            copied_path = os.path.join(test_dst, "large_file.bin")
            self.assertTrue(os.path.exists(copied_path))
            self.assertEqual(os.path.getsize(copied_path), original_size)

    def test_generate_public_create_destination(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create source dir inside temp_dir
            test_src = os.path.join(temp_dir, "source")
            os.makedirs(test_src)

            # Define a destination that doesn't exist yet
            test_dst = os.path.join(temp_dir, "destination")

            # Create a test file
            with open(os.path.join(test_src, "file1.txt"), "w") as f:
                f.write("Test content")

            # Call function (should create the destination directory)
            generate_public(test_src, test_dst)

            # Verify destination was created and file was copied
            self.assertTrue(os.path.exists(test_dst))
            self.assertTrue(os.path.exists(os.path.join(test_dst, "file1.txt")))


if __name__ == "__main__":
    unittest.main()