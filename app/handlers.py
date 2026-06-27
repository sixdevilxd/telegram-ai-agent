import logging
import os
import tempfile

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

from config import BOT_NAME
from core.agent import Agent
from core.permissions import is_admin
from services.memory_service import clear_user_memory, count_messages, count_users
from services.note_service import add_note, clear_notes, count_notes, list_notes
from services.persona_service import clear_persona, get_persona, set_persona
from services.telegram_service import send_long_message
from tools.calculator import calculate
from tools.file_reader import read_text_file
from tools.web_search import web_search

logger = logging.getLogger(__name__)
agent = Agent()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Halo, saya {BOT_NAME}.\n\n"
        "V4 aktif: auto tool routing, file reader, persona mode.\n\n"
        "Coba langsung ketik:\n"
        "- hitung 25000*3\n"
        "- cari berita AI terbaru\n"
        "- catat ide bisnis bot telegram\n\n"
        "Ketik /help untuk command lengkap."
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Command:\n\n"
        "/start - mulai bot\n"
        "/help - bantuan\n"
        "/reset - reset memory chat\n"
        "/status - cek bot aktif\n"
        "/id - tampilkan Telegram user ID\n"
        "/search kata kunci - web search\n"
        "/calc ekspresi - kalkulator\n"
        "/note isi catatan - simpan catatan\n"
        "/notes - tampilkan catatan\n"
        "/clearnotes - hapus catatan\n"
        "/persona gaya jawaban - set persona\n"
        "/persona - lihat persona\n"
        "/clearpersona - hapus persona\n\n"
        "Auto routing tanpa command:\n"
        "- hitung 10*5\n"
        "- cari harga bitcoin terbaru\n"
        "- catat beli paket internet\n\n"
        "Kirim file .txt/.md/.csv/.json/.py untuk diringkas.\n\n"
        "Admin only: /stats"
    )
    await update.message.reply_text(text)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_user_memory(update.effective_user.id)
    await update.message.reply_text("Memory percakapan kamu sudah dihapus.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{BOT_NAME} v4 aktif. Groq + tools + memory siap digunakan.")


async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Telegram user ID kamu: {update.effective_user.id}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Command ini khusus admin.")
        return
    await update.message.reply_text(
        "Statistik bot:\n"
        f"- Total user: {count_users()}\n"
        f"- Total pesan: {count_messages()}\n"
        f"- Total catatan: {count_notes()}"
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).strip()
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await send_long_message(update, web_search(query))


async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(calculate(" ".join(context.args).strip()))


async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    content = " ".join(context.args).strip()
    if not content:
        await update.message.reply_text("Contoh: /note beli paket internet besok")
        return
    add_note(update.effective_user.id, content)
    await update.message.reply_text("Catatan tersimpan.")


async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rows = list_notes(update.effective_user.id)
    if not rows:
        await update.message.reply_text("Belum ada catatan.")
        return
    lines = ["Catatan terakhir:"]
    for idx, (_, content, created_at) in enumerate(rows, start=1):
        lines.append(f"{idx}. {content}\n   {created_at}")
    await send_long_message(update, "\n\n".join(lines))


async def clearnotes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_notes(update.effective_user.id)
    await update.message.reply_text("Semua catatan kamu sudah dihapus.")


async def persona(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    value = " ".join(context.args).strip()
    if not value:
        current = get_persona(user) or "Belum ada persona aktif."
        await update.message.reply_text(f"Persona saat ini: {current}")
        return
    set_persona(user, value)
    await update.message.reply_text("Persona disimpan.")


async def clearpersona(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clear_persona(update.effective_user.id)
    await update.message.reply_text("Persona dihapus.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        tg_file = await doc.get_file()
        suffix = os.path.splitext(doc.file_name or "file.txt")[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            path = tmp.name
        await tg_file.download_to_drive(path)
        content = read_text_file(path)
        prompt = f"Ringkas dan jelaskan isi file ini dalam bahasa Indonesia:\n\n{content}"
        reply = agent.respond(update.effective_user.id, prompt)
    except Exception:
        logger.exception("Failed reading document")
        reply = "Gagal membaca file. Pastikan formatnya .txt, .md, .csv, .json, .py, atau .log"
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
    await send_long_message(update, reply)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_value = update.effective_user.id
    user_text = update.message.text
    logger.info("Message from user_id=%s", user_id_value)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        reply = agent.respond(user_id=user_id_value, user_text=user_text)
    except Exception:
        logger.exception("Failed to handle message from user_id=%s", user_id_value)
        reply = "Maaf, terjadi gangguan. Cek logs/bot.log atau API key Groq."

    await send_long_message(update, reply)


def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("id", user_id))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("calc", calc))
    app.add_handler(CommandHandler("note", note))
    app.add_handler(CommandHandler("notes", notes))
    app.add_handler(CommandHandler("clearnotes", clearnotes))
    app.add_handler(CommandHandler("persona", persona))
    app.add_handler(CommandHandler("clearpersona", clearpersona))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
