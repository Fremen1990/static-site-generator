import os

from src.generate_page import generate_page


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath:str)-> None:
    entries = os.listdir(dir_path_content)

    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)

        relative_path = os.path.relpath(entry_path, dir_path_content)
        dest_path = os.path.join(dest_dir_path, relative_path)

        # Check if the entry is in a file
        if os.path.isfile(entry_path):
            if entry_path.endswith(".md"):
                dest_html_path = os.path.splitext(dest_path)[0] + ".html"
                generate_page(entry_path, template_path, dest_html_path, basepath)
        # If it's a directory, recursively process it
        elif os.path.isdir(entry_path):
            # Ensure the corresponding directory exists in destination
            os.makedirs(os.path.join(dest_dir_path, relative_path), exist_ok=True)
            # Recursively process the subdirectory
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, relative_path), basepath)


