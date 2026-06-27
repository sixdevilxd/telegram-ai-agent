def _split_text(text: str, chunk_size: int):
    """Pisahkan teks panjang berdasarkan baris terdekat agar tag Markdown tidak terpotong di tengah."""
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

    for part in _split_text(text, chunk_size):
        if not part.strip():
            continue
        try:
            # Coba kirim dengan format Markdown agar **tebal**, kode, dll tampil rapi.
            await update.message.reply_text(part, parse_mode="Markdown")
        except Exception:
            # Fallback: jika Markdown tidak valid, kirim sebagai teks polos.
            await update.message.reply_text(part)
