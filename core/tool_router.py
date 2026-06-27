import re

from services.note_service import add_note
from tools.calculator import calculate
from tools.web_search import web_search


def route_tool(user_id: int, text: str):
    lower = text.lower().strip()

    calc_match = re.search(r"(?:hitung|calculate|calc)\s+(.+)", lower)
    if calc_match:
        expr = calc_match.group(1)
        if re.fullmatch(r"[0-9\s+\-*/().%]+", expr):
            return calculate(expr.replace("%", "/100"))

    if lower.startswith(("cari ", "search ", "web ")):
        query = re.sub(r"^(cari|search|web)\s+", "", text, flags=re.I).strip()
        return web_search(query)

    if lower.startswith(("catat ", "note ", "ingat ")):
        note = re.sub(r"^(catat|note|ingat)\s+", "", text, flags=re.I).strip()
        if note:
            add_note(user_id, note)
            return "Catatan tersimpan."

    return None
