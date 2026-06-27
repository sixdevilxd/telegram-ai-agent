import os

import httpx

GMGN_BASE = "https://gmgn.ai/defi/quotation/v1"
GMGN_COOKIE = os.getenv("GMGN_COOKIE", "")
GMGN_USER_AGENT = os.getenv(
    "GMGN_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
)

CHAIN_MAP = {
    "sol": "sol", "solana": "sol",
    "eth": "eth", "ethereum": "eth",
    "bsc": "bsc", "bnb": "bsc",
    "base": "base",
    "tron": "tron",
}


def _fmt(n):
    try:
        n = float(n)
    except Exception:
        return str(n)
    if abs(n) >= 1_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    if abs(n) >= 1_000_000:
        return f"{n/1_000_000:.2f}M"
    if abs(n) >= 1_000:
        return f"{n/1_000:.2f}K"
    if abs(n) < 1:
        return f"{n:.6f}".rstrip("0").rstrip(".")
    return f"{n:.2f}"


def gmgn_trending(chain: str = "sol", time_period: str = "1h") -> str:
    chain = CHAIN_MAP.get(chain.strip().lower(), "sol")
    url = f"{GMGN_BASE}/rank/{chain}/swaps/{time_period}"
    params = {
        "orderby": "swaps",
        "direction": "desc",
        "filters[]": "not_honeypot",
    }
    headers = {
        "User-Agent": GMGN_USER_AGENT,
        "Accept": "application/json",
        "Referer": "https://gmgn.ai/",
    }
    if GMGN_COOKIE:
        headers["Cookie"] = GMGN_COOKIE

    fallback = (
        "GMGN diblok Cloudflare dari Termux.\n"
        "Buka langsung:\n"
        f"https://gmgn.ai/?chain={chain}\n\n"
        "Tips: isi GMGN_COOKIE di .env agar request berhasil (cookie expired harian).\n"
        "Untuk new launch stabil, pakai /newpairs (DexScreener)."
    )

    try:
        with httpx.Client(timeout=40, follow_redirects=True) as c:
            r = c.get(url, params=params, headers=headers)
        if r.status_code in (403, 401, 429):
            return fallback
        r.raise_for_status()
        data = r.json()
    except Exception:
        return fallback

    rank = (data.get("data") or {}).get("rank") or []
    if not rank:
        return fallback

    lines = [f"GMGN trending {chain.upper()} ({time_period}):"]
    for i, t in enumerate(rank[:10], 1):
        lines.append(
            f"{i}. {t.get('symbol','?')} | ${_fmt(t.get('price'))} | "
            f"{float(t.get('price_change_percent', 0) or 0):.1f}% | "
            f"swaps {t.get('swaps','-')} | holders {t.get('holders','-')}\n"
            f"   https://gmgn.ai/{chain}/token/{t.get('address','')}"
        )
    return "\n".join(lines)
