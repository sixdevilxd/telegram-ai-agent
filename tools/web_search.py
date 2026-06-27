import html
import re
from urllib.parse import quote_plus

import httpx


def web_search(query: str, max_results: int = 5) -> str:
    if not query.strip():
        return "Masukkan query. Contoh: /search berita AI terbaru"

    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        with httpx.Client(timeout=20, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
    except Exception as exc:
        return f"Gagal melakukan web search: {exc}"

    pattern = re.compile(
        r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>',
        re.DOTALL,
    )
    matches = pattern.findall(response.text)

    if not matches:
        return "Tidak menemukan hasil search. Coba kata kunci lain."

    lines = [f"Hasil web search untuk: {query}\n"]
    for idx, (link, title) in enumerate(matches[:max_results], start=1):
        clean_title = re.sub(r"<.*?>", "", title)
        clean_title = html.unescape(clean_title).strip()
        clean_link = html.unescape(link).strip()
        lines.append(f"{idx}. {clean_title}\n{clean_link}")

    return "\n\n".join(lines)
