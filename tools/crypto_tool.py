import os

import httpx

CG_BASE = "https://api.coingecko.com/api/v3"
DS_BASE = "https://api.dexscreener.com"
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")

UA = {"User-Agent": "Mozilla/5.0 (Linux; Android; Termux)", "Accept": "application/json"}


def _get(url, params=None, headers=None):
    h = dict(UA)
    if headers:
        h.update(headers)
    last = None
    for verify in (True, False):
        try:
            with httpx.Client(timeout=40, follow_redirects=True, verify=verify) as c:
                r = c.get(url, params=params, headers=h)
                r.raise_for_status()
                return r.json()
        except Exception as e:
            last = e
            continue
    raise RuntimeError(last)


def _fmt_num(n):
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
        return f"{n:.8f}".rstrip("0").rstrip(".")
    return f"{n:.2f}"


def price(query: str) -> str:
    query = query.strip().lower()
    if not query:
        return "Contoh: /price bitcoin"
    try:
        search = _get(f"{CG_BASE}/search", {"query": query})
        coins = search.get("coins", [])
        if not coins:
            return f"Koin '{query}' tidak ditemukan di CoinGecko."
        coin_id = coins[0]["id"]
        data = _get(
            f"{CG_BASE}/coins/markets",
            {"vs_currency": "usd", "ids": coin_id},
        )
        if not data:
            return f"Data harga '{query}' tidak tersedia."
        d = data[0]
        return (
            f"{d['name']} ({d['symbol'].upper()})\n"
            f"Harga: ${_fmt_num(d.get('current_price'))}\n"
            f"24h: {d.get('price_change_percentage_24h', 0):.2f}%\n"
            f"Market Cap: ${_fmt_num(d.get('market_cap'))}\n"
            f"Volume 24h: ${_fmt_num(d.get('total_volume'))}\n"
            f"Rank: #{d.get('market_cap_rank', '-')}\n"
            f"ATH: ${_fmt_num(d.get('ath'))}"
        )
    except Exception as e:
        return f"Gagal ambil harga: {e}"


def coin_detail(query: str) -> str:
    return price(query)


def trending() -> str:
    try:
        data = _get(f"{CG_BASE}/search/trending")
        coins = data.get("coins", [])[:10]
        if not coins:
            return "Tidak ada data trending."
        lines = ["Trending CoinGecko:"]
        for i, c in enumerate(coins, 1):
            item = c.get("item", {})
            lines.append(f"{i}. {item.get('name')} ({item.get('symbol','').upper()}) - rank #{item.get('market_cap_rank','-')}")
        return "\n".join(lines)
    except Exception as e:
        return f"Gagal ambil trending: {e}"


def new_pairs(chain: str = "") -> str:
    chain = chain.strip().lower()
    try:
        # DexScreener latest token profiles, then enrich with pair data.
        profiles = _get(f"{DS_BASE}/token-profiles/latest/v1")
        if isinstance(profiles, dict):
            profiles = profiles.get("profiles", []) or []
        if chain:
            profiles = [p for p in profiles if str(p.get("chainId", "")).lower() == chain]
        profiles = profiles[:10]
        if not profiles:
            return f"Tidak ada new pairs{(' di ' + chain) if chain else ''}. Coba: /newpairs solana"
        lines = [f"New tokens/launch{(' - ' + chain) if chain else ''} (DexScreener):"]
        for i, p in enumerate(profiles, 1):
            lines.append(
                f"{i}. {p.get('chainId','?')} | {p.get('tokenAddress','')[:10]}...\n   {p.get('url','')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Gagal ambil new pairs: {e}"


def token_info(address: str) -> str:
    address = address.strip()
    if not address:
        return "Contoh: /token <alamat_kontrak>"
    try:
        data = _get(f"{DS_BASE}/latest/dex/tokens/{address}")
        pairs = data.get("pairs") or []
        if not pairs:
            return f"Token {address[:12]}... tidak ditemukan di DexScreener."
        p = pairs[0]
        base = p.get("baseToken", {})
        return (
            f"{base.get('name','?')} ({base.get('symbol','?')})\n"
            f"Chain: {p.get('chainId')}\n"
            f"DEX: {p.get('dexId')}\n"
            f"Harga: ${_fmt_num(p.get('priceUsd'))}\n"
            f"Liquidity: ${_fmt_num((p.get('liquidity') or {}).get('usd'))}\n"
            f"FDV: ${_fmt_num(p.get('fdv'))}\n"
            f"Vol 24h: ${_fmt_num((p.get('volume') or {}).get('h24'))}\n"
            f"Change 24h: {(p.get('priceChange') or {}).get('h24','-')}%\n"
            f"{p.get('url','')}"
        )
    except Exception as e:
        return f"Gagal ambil token: {e}"


def dex_search(query: str) -> str:
    query = query.strip()
    if not query:
        return "Contoh: /dex pepe"
    try:
        data = _get(f"{DS_BASE}/latest/dex/search", {"q": query})
        pairs = (data.get("pairs") or [])[:8]
        if not pairs:
            return f"Tidak ada hasil DEX untuk '{query}'."
        lines = [f"Hasil DEX untuk: {query}"]
        for i, p in enumerate(pairs, 1):
            base = p.get("baseToken", {})
            lines.append(
                f"{i}. {base.get('symbol','?')} on {p.get('chainId')}/{p.get('dexId')} - ${_fmt_num(p.get('priceUsd'))} | liq ${_fmt_num((p.get('liquidity') or {}).get('usd'))}\n   {p.get('url','')}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Gagal cari DEX: {e}"


def gmgn_link(address: str) -> str:
    address = address.strip()
    if not address:
        return "Contoh: /gmgn <alamat_kontrak>"
    return (
        f"Quick links untuk {address[:12]}...:\n"
        f"GMGN: https://gmgn.ai/sol/token/{address}\n"
        f"Birdeye: https://birdeye.so/token/{address}\n"
        f"DexScreener: https://dexscreener.com/search?q={address}"
    )
