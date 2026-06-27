import html
import re
from urllib.parse import quote_plus

import httpx


def _extract_results(page_html: str, max_results: int):
    patterns = [
        re.compile(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', re.DOTALL),
        re.compile(r'<a class="result-link" href="(.*?)">(.*?)</a>', re.DOTALL),
        re.compile(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', re.DOTALL),
    ]

    results = []
    seen = set()
    for pattern in patterns:
        for link, title in pattern.findall(page_html):
            clean_title = re.sub(r"<.*?>", "", title)
            clean_title = html.unescape(clean_title).strip()
            clean_link = html.unescape(link).strip()

            if "duckduckgo.com" in clean_link and "uddg=" in clean_link:
                try:
                    from urllib.parse import parse_qs, urlparse, unquote
                    qs = parse_qs(urlparse(clean_link).query)
                    clean_link = unquote(qs.get("uddg", [clean_link])[0])
                except Exception:
                    pass

            if clean_title and clean_link and clean_link not in seen:
                seen.add(clean_link)
                results.append((clean_title, clean_link))
            if len(results) >= max_results:
                return results
    return results


def _fetch(url: str, headers: dict, verify_ssl: bool):
    with httpx.Client(timeout=45, follow_redirects=True, verify=verify_ssl) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        return response.text


def web_search(query: str, max_results: int = 5) -> str:
    if not query.strip():
        return "Masukkan query. Contoh: /search berita AI terbaru"

    encoded_query = quote_plus(query)
    urls = [
        f"https://lite.duckduckgo.com/lite/?q={encoded_query}",
        f"https://html.duckduckgo.com/html/?q={encoded_query}",
        f"https://duckduckgo.com/html/?q={encoded_query}",
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android; Termux) AppleWebKit/537.36 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "close",
    }

    errors = []

    # First try normal SSL verification, then fallback verify=False for Termux SSL EOF issues.
    for verify_ssl in [True, False]:
        for url in urls:
            try:
                page = _fetch(url, headers, verify_ssl)
                results = _extract_results(page, max_results)
                if results:
                    lines = [f"Hasil web search untuk: {query}\n"]
                    for idx, (title, link) in enumerate(results, start=1):
                        lines.append(f"{idx}. {title}\n{link}")
                    if not verify_ssl:
                        lines.append("\nCatatan: search memakai fallback SSL Termux.")
                    return "\n\n".join(lines)
            except Exception as exc:
                errors.append(str(exc))
                continue

    last = errors[-1] if errors else "unknown error"
    return (
        "Gagal melakukan web search.\n"
        f"Detail terakhir: {last}\n\n"
        "Solusi Termux yang bisa dicoba:\n"
        "1. pkg update && pkg upgrade -y\n"
        "2. pkg install ca-certificates openssl -y\n"
        "3. Coba jaringan lain atau aktifkan VPN."
    )
