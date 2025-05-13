import os
import re

from src.extract_title import extract_title
from src.markdown_to_html_node import markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_file = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_file = f.read()

    title = extract_title(markdown_file)
    html_string = markdown_to_html_node(markdown_file).to_html()


    template_file_with_new_title = template_file.replace("{{ Title }}", title)
    template_file_with_new_content = template_file_with_new_title.replace("{{ Content }}", html_string)

    # Make sure basepath ends with a slash if it's not empty
    if basepath and not basepath.endswith('/'):
        basepath += '/'

    # Debug: Print the basepath for verification
    print(f"Replacing paths with basepath: {basepath}")

    # Replace all href attributes that start with a slash
    template_file_with_new_content = re.sub(r'href="/', f'href="{basepath}', template_file_with_new_content)

    # Replace all src attributes that start with a slash
    template_file_with_new_content = re.sub(r'src="/', f'src="{basepath}', template_file_with_new_content)


    dir_name = os.path.dirname(dest_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_file_with_new_content)
