import html
import re


def to_telegram_html(text: str) -> str:
    """Konversi Markdown gaya LLM menjadi HTML yang aman & rapi untuk Telegram."""
    if not text:
        return ""

    placeholders = {}

    def _store(tag_html):
        key = f"\x00{len(placeholders)}\x00"
        placeholders[key] = tag_html
        return key

    # 1) Code block ```...```
    def _codeblock(m):
        return _store(f"<pre><code>{html.escape(m.group(2))}</code></pre>")

    text = re.sub(r"```([a-zA-Z0-9_+-]*)\n?(.*?)```", _codeblock, text, flags=re.DOTALL)

    # 2) Inline code `...`
    text = re.sub(r"`([^`\n]+?)`", lambda m: _store(f"<code>{html.escape(m.group(1))}</code>"), text)

    # 3) Link [teks](url)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^\s)]+)\)",
        lambda m: _store(f'<a href="{html.escape(m.group(2), quote=True)}">{html.escape(m.group(1))}</a>'),
        text,
    )

    # 4) Escape sisa teks
    text = html.escape(text)

    # 5) Heading -> bold
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s*(.+?)\s*#*$", r"<b>\1</b>", text)

    # 6) Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text, flags=re.DOTALL)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text, flags=re.DOTALL)

    # 7) Italic
    text = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<i>\1</i>", text)
    text = re.sub(r"(?<![_\w])_(?!\s)(.+?)(?<!\s)_(?![_\w])", r"<i>\1</i>", text)

    # 8) Strikethrough
    text = re.sub(r"~~(.+?)~~", r"<s>\1</s>", text)

    # 9) Bullet -> bullet point
    text = re.sub(r"(?m)^(\s*)[-*]\s+", "\\1\u2022 ", text)

    # 10) Blockquote
    text = re.sub(r"(?m)^&gt;\s?(.*)$", r"<i>\1</i>", text)

    for key, val in placeholders.items():
        text = text.replace(key, val)
    return text


def _split_text(text: str, chunk_size: int):
    """Pisahkan teks panjang berdasarkan baris terdekat agar tag/format tidak terpotong."""
    parts = []
    while text:
        if len(text) <= chunk_size:
            parts.append(text)
            break
        cut = text.rfind("\n", 0, chunk_size)
        if cut <= 0:
            cut = chunk_size
        parts.append(text[:cut])
        text = text[cut:].lstrip("\n")
    return parts


async def send_long_message(update, text: str, chunk_size: int = 3900):
    if not text:
        text = "Tidak ada respons."

    # Potong dulu berbasis Markdown mentah (per baris) lalu konversi tiap bagian ke HTML.
    for part in _split_text(text, chunk_size):
        if not part.strip():
            continue
        try:
            await update.message.reply_text(to_telegram_html(part), parse_mode="HTML")
        except Exception:
            # Fallback: kirim teks polos jika HTML gagal di-parse.
            await update.message.reply_text(part)
