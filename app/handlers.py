from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

from config import BOT_NAME
from core.agent import Agent
from services.memory_service import clear_user_memory
from services.telegram_service import send_long_message

agent = Agent()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"Halo, saya {BOT_NAME}.\n\n"
        "Kirim pesan apa saja untuk mulai chat.\n\n"
        "Command:\n"
        "/help - bantuan\n"
        "/reset - hapus memory percakapan\n"
        "/status - cek status bot"
    )
    await update.message.reply_text(text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Bantuan command:\n\n"
        "/start - mulai bot\n"
        "/help - tampilkan bantuan\n"
        "/reset - reset memory chat kamu\n"
        "/status - cek bot aktif\n\n"
        "Kamu bisa tanya coding, ide bisnis, riset, strategi, atau hal lain."
    )
    await update.message.reply_text(text)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    clear_user_memory(user_id)
    await update.message.reply_text("Memory percakapan kamu sudah dihapus.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{BOT_NAME} aktif dan siap digunakan.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        reply = agent.respond(user_id=user_id, user_text=user_text)
    except Exception as exc:
        reply = f"Maaf, terjadi error: {exc}"

    await send_long_message(update, reply)


def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
