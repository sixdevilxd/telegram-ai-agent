import re

from services.note_service import add_note
from tools.calculator import calculate
from tools.crypto_tool import new_pairs, price, token_info
from tools.social_search import social_search
from tools.web_search import web_search


def route_tool(user_id: int, text: str):
    lower = text.lower().strip()

    calc_match = re.search(r"(?:hitung|calculate|calc)\s+(.+)", lower)
    if calc_match:
        expr = calc_match.group(1)
        if re.fullmatch(r"[0-9\s+\-*/().%]+", expr):
            return calculate(expr.replace("%", "/100"))

    price_match = re.search(r"(?:harga|price)\s+([a-z0-9 ]+)", lower)
    if price_match:
        return price(price_match.group(1))

    np_match = re.search(r"new\s*pairs?\s*([a-z]*)", lower)
    if np_match:
        return new_pairs(np_match.group(1))

    tok_match = re.search(r"(?:cek token|token)\s+([A-Za-z0-9]{20,})", text)
    if tok_match:
        return token_info(tok_match.group(1))

    if lower.startswith(("cari ", "search ", "web ")):
        query = re.sub(r"^(cari|search|web)\s+", "", text, flags=re.I).strip()
        return web_search(query)

    social_match = re.search(r"(?:cari di|search di|search on)\s+(twitter|x|linkedin|reddit|facebook|instagram|tiktok|youtube)\s+(.+)", lower)
    if social_match:
        return social_search(social_match.group(1), social_match.group(2))

    if lower.startswith(("catat ", "note ", "ingat ")):
        note = re.sub(r"^(catat|note|ingat)\s+", "", text, flags=re.I).strip()
        if note:
            add_note(user_id, note)
            return "Catatan tersimpan."

    return None
