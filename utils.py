import fitz 

def extract_text(filepath):
    if filepath.endswith(".pdf"):
        with fitz.open(filepath) as doc:
            return "\n".join([page.get_text() for page in doc])
    elif filepath.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""
