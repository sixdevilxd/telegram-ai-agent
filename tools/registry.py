"""Registry tool untuk function-calling agent.

TOOL_SCHEMAS: definisi tool (OpenAI/Groq compatible) yang dikirim ke LLM.
execute_tool(): mengeksekusi tool berdasarkan nama yang diminta LLM.
"""

from services.note_service import add_note, list_notes
from tools.calculator import calculate
from tools.crypto_tool import dex_search, new_pairs, price, token_info, trending
from tools.social_search import social_search
from tools.web_search import web_search

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_crypto_price",
            "description": "Ambil harga, market cap, volume, dan rank sebuah koin crypto dari CoinGecko. Pakai untuk pertanyaan harga koin populer (bitcoin, ethereum, solana, dll).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Nama atau simbol koin, mis. 'bitcoin' atau 'btc'"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_trending_coins",
            "description": "Ambil daftar koin yang sedang trending di CoinGecko.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_new_pairs",
            "description": "Ambil token/launch baru dari DexScreener, opsional difilter per chain (solana, ethereum, bsc, base).",
            "parameters": {
                "type": "object",
                "properties": {
                    "chain": {"type": "string", "description": "Nama chain opsional, mis. 'solana'. Kosongkan untuk semua chain."}
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_token_info",
            "description": "Ambil detail token berdasarkan alamat kontrak (harga, liquidity, FDV, volume) dari DexScreener.",
            "parameters": {
                "type": "object",
                "properties": {
                    "address": {"type": "string", "description": "Alamat kontrak token"}
                },
                "required": ["address"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_dex",
            "description": "Cari pair/token di DexScreener berdasarkan nama atau simbol (mis. 'pepe').",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Cari informasi terbaru di web (DuckDuckGo). Pakai untuk berita, fakta terkini, atau info yang tidak kamu ketahui.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Hitung ekspresi matematika sederhana, mis. '25000*3+10000'.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_social",
            "description": "Buat link pencarian di platform sosial (x, twitter, linkedin, reddit, facebook, youtube, tiktok, instagram).",
            "parameters": {
                "type": "object",
                "properties": {
                    "platform": {"type": "string"},
                    "query": {"type": "string"},
                },
                "required": ["platform", "query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "Simpan catatan/pengingat milik user.",
            "parameters": {
                "type": "object",
                "properties": {"content": {"type": "string"}},
                "required": ["content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_my_notes",
            "description": "Tampilkan catatan terakhir milik user.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


def execute_tool(name: str, args: dict, user_id: int) -> str:
    args = args or {}
    try:
        if name == "get_crypto_price":
            return price(args.get("query", ""))
        if name == "get_trending_coins":
            return trending()
        if name == "get_new_pairs":
            return new_pairs(args.get("chain", ""))
        if name == "get_token_info":
            return token_info(args.get("address", ""))
        if name == "search_dex":
            return dex_search(args.get("query", ""))
        if name == "web_search":
            return web_search(args.get("query", ""))
        if name == "calculate":
            return calculate(args.get("expression", ""))
        if name == "search_social":
            return social_search(args.get("platform", ""), args.get("query", ""))
        if name == "save_note":
            content = args.get("content", "").strip()
            if not content:
                return "Catatan kosong."
            add_note(user_id, content)
            return "Catatan tersimpan."
        if name == "list_my_notes":
            rows = list_notes(user_id)
            if not rows:
                return "Belum ada catatan."
            return "\n".join(f"- {c}" for _, c, _ in rows)
        return f"Tool '{name}' tidak dikenal."
    except Exception as exc:
        return f"Tool '{name}' error: {exc}"
