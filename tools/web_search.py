import html
import re
from urllib.parse import quote_plus

import httpx


def _extract_results(page_html: str, max_results: int):
    patterns = [
        re.compile(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', re.DOTALL),
        re.compile(r'<a class="result-link" href="(.*?)">(.*?)</a>', re.DOTALL),
    ]

    results = []
    for pattern in patterns:
        for link, title in pattern.findall(page_html):
            clean_title = re.sub(r"<.*?>", "", title)
            clean_title = html.unescape(clean_title).strip()
            clean_link = html.unescape(link).strip()
            if clean_title and clean_link:
                results.append((clean_title, clean_link))
            if len(results) >= max_results:
                return results
    return results


def web_search(query: str, max_results: int = 5) -> str:
    if not query.strip():
        return "Masukkan query. Contoh: /search berita AI terbaru"

    encoded_query = quote_plus(query)
    urls = [
        f"https://lite.duckduckgo.com/lite/?q={encoded_query}",
        f"https://duckduckgo.com/html/?q={encoded_query}",
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    last_error = None
    for url in urls:
        try:
            with httpx.Client(timeout=45, follow_redirects=True) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()

            results = _extract_results(response.text, max_results)
            if results:
                lines = [f"Hasil web search untuk: {query}\n"]
                for idx, (title, link) in enumerate(results, start=1):
                    lines.append(f"{idx}. {title}\n{link}")
                return "\n\n".join(lines)
        except Exception as exc:
            last_error = exc
            continue

    return (
        "Gagal melakukan web search atau tidak menemukan hasil.\n"
        f"Detail terakhir: {last_error}\n\n"
        "Coba lagi dengan kata kunci lebih pendek, atau cek koneksi internet Termux."
    )
