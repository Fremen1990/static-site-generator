def extract_title(markdown: str)-> str:
    list_of_lines = markdown.splitlines()

    for line in list_of_lines:
        line = line.strip()
        if line.startswith("# "):
            h1 = line.replace("# ", "", 1)
            result = h1.strip()
            return result

    raise Exception("There is no header")