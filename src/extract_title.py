def extract_title(markdown):
    lines = markdown.splitlines()

    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            if not title:
                raise ValueError("H1 header found but no text provided.")
            return title
    raise ValueError("No H1 header found in the markdown.")