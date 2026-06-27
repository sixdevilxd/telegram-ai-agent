from tools.crypto_tool import dex_search, token_info
from tools.web_search import web_search


def build_narrative_context(query: str) -> str:
    query = query.strip()
    if not query:
        return ""

    # Jika terlihat seperti contract address, pakai token_info; selain itu dex_search.
    if len(query) >= 20 and " " not in query:
        market = token_info(query)
    else:
        market = dex_search(query)

    web = web_search(f"{query} crypto token narrative project info", max_results=5)

    return (
        "=== DATA PASAR / DEX ===\n"
        f"{market}\n\n"
        "=== KONTEKS WEB ===\n"
        f"{web}"
    )


NARRATIVE_PROMPT = """
Kamu adalah analis kripto. Analisis NARASI token berikut berdasarkan data pasar dan konteks web.
Jawab dalam bahasa Indonesia, ringkas, terstruktur, dan tidak mengarang data.

Format jawaban:
1. Identitas token (nama, simbol, chain jika ada)
2. Kategori & tema narasi (contoh: AI, memecoin, RWA, DeFi, gaming, DePIN, dll)
3. Kekuatan momentum (berdasarkan volume, likuiditas, perubahan harga)
4. Sentimen pasar (positif/netral/negatif dan alasannya)
5. Potensi & katalis narasi
6. Sinyal risiko (likuiditas tipis, hype berlebihan, data minim, dll)
7. Kesimpulan singkat

Akhiri dengan disclaimer: "Ini analisis naratif berbasis AI, bukan saran finansial. DYOR."

DATA:
{context}
""".strip()


def narrative_prompt(query: str, context: str) -> str:
    return NARRATIVE_PROMPT.format(context=context) + f"\n\nToken yang dianalisis: {query}"
