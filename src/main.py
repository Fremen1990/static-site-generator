import os.path
import shutil
import sys

from src.generate_pages_recursive import generate_pages_recursive

SOURCE = "static"
DESTINATION = "docs"

FROM_PATH = "content"
TEMPLATE_PATH = "template.html"
DEST_PATH = os.path.join(DESTINATION)


def generate_public(source=SOURCE, destination=DESTINATION):
    if not os.path.exists(source):
        raise Exception("No source 'static' directory")

    if os.path.exists(destination):
        shutil.rmtree(destination)

    if not os.path.exists(destination):
        os.mkdir(destination)

    copy_static_to_public(source, destination)
    files_after_coping = os.listdir(destination)
    print(f"\n Files and directories created in destination {destination}: \n {files_after_coping} \n")
    return None


def copy_static_to_public(source:str, destination:str):
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)

        is_file =     os.path.isfile(src_path)

        if not is_file:
            os.makedirs(dst_path, exist_ok=True)
            copy_static_to_public(src_path, dst_path)

        if is_file:
            shutil.copy(src_path, dst_path)
            print(f"File: {item}, has been copied from {source} to {destination}")


def main()-> None:
    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    generate_public()
    generate_pages_recursive(FROM_PATH, TEMPLATE_PATH, DEST_PATH, basepath=basepath)

if __name__ == "__main__":
    main()


