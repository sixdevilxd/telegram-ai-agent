import os

MAX_CHARS = 12000


def read_text_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext not in [".txt", ".md", ".csv", ".json", ".py", ".log"]:
        return "Format file belum didukung. Kirim .txt, .md, .csv, .json, .py, atau .log"

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(MAX_CHARS)

    if not content.strip():
        return "File kosong atau tidak bisa dibaca."

    return content
