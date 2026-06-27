async def send_long_message(update, text: str, chunk_size: int = 3900):
    if not text:
        text = "Tidak ada respons."

    for i in range(0, len(text), chunk_size):
        await update.message.reply_text(text[i : i + chunk_size])
