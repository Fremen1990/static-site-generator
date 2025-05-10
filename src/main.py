import os.path
import shutil

from textnode import TextNode, TextType


def copy_static_to_public()-> None:
    if os.path.exists("static") == False:
        print("No static directory")
        return Exception("No 'static' directory")



    if os.path.exists("public") == True:
        shutil.rmtree('public')

    if os.path.exists("public") == False:
        os.mkdir("public")


    shutil.copy("static/index.css", "public")
    os.mkdir("public/images")
    shutil.copy("static/images/tolkien.png", "public/images/tolkien.png")
    return None


def main()-> None:
    # node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    # print(node)

    copy_static_to_public()

if __name__ == "__main__":
    main()


