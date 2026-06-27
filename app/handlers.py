import logging
import os
import tempfile

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters

from config import BOT_NAME
from core.agent import Agent
from core.permissions import is_admin
from services.groq_provider import GroqProvider
from services.memory_service import clear_user_memory, count_messages, count_users
from services.note_service import add_note, clear_notes, count_notes, list_notes
from services.persona_service import clear_persona, get_persona, set_persona
from services.telegram_service import send_long_message
from services.user_service import list_user_ids, list_users, upsert_user
from tools.calculator import calculate
from tools.crypto_tool import coin_detail, dex_search, gmgn_link, new_pairs, price, token_info, trending
from tools.file_reader import read_text_file
from tools.shell_tool import run_shell
from tools.social_search import platform_guide, social_prompt, social_search
from tools.system_info import system_info
from tools.web_search import web_search

logger = logging.getLogger(__name__)
agent = Agent()
vision_ai = GroqProvider()


def track_user(update: Update):
    u = update.effective_user
    if u:
        upsert_user(u.id, u.username or "", u.first_name or "")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    await update.message.reply_text(
        f"{BOT_NAME} v8 aktif.\n\n"
        "Fitur: chat AI, vision, social intelligence, dan crypto real-time (CoinGecko + DexScreener).\n"
        "Ketik /help untuk command lengkap."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    await update.message.reply_text(
        "Command v8:\n"
        "Crypto:\n"
        "/price bitcoin - harga & market\n"
        "/coin pepe - detail koin\n"
        "/trending - koin trending\n"
        "/newpairs solana - new pairs/launch\n"
        "/token <kontrak> - info token DEX\n"
        "/dex pepe - cari pair di DEX\n"
        "/gmgn <kontrak> - quick links gmgn/birdeye\n\n"
        "AI & web:\n"
        "/asksearch topik, /search query\n"
        "/social platform query, /socialprompt platform topik, /platform nama\n"
        "/calc, /note, /notes, /clearnotes, /persona, /clearpersona\n"
        "/id, /status, /reset\n\n"
        "Media: kirim foto/gambar atau file teks.\n\n"
        "Admin: /stats, /users, /broadcast, /shell, /sysinfo\n\n"
        "Auto: harga bitcoin, new pairs solana, cek token <kontrak>, cari di reddit groq."
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); clear_user_memory(update.effective_user.id); await update.message.reply_text("Memory chat dihapus.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await update.message.reply_text(f"{BOT_NAME} v8 aktif: text + vision + social + crypto siap.")


async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await update.message.reply_text(f"Telegram user ID kamu: {update.effective_user.id}")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    if not is_admin(update.effective_user.id): return await update.message.reply_text("Khusus admin.")
    await update.message.reply_text(f"Stats:\n- Users chat: {count_users()}\n- Messages: {count_messages()}\n- Notes: {count_notes()}\n- Known users: {len(list_user_ids())}")


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    if not is_admin(update.effective_user.id): return await update.message.reply_text("Khusus admin.")
    rows = list_users()
    text = "Users terakhir:\n" + "\n".join(f"- {uid} @{username} {first_name} | {last_seen}" for uid, username, first_name, last_seen in rows) if rows else "Belum ada user."
    await send_long_message(update, text)


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    if not is_admin(update.effective_user.id): return await update.message.reply_text("Khusus admin.")
    message = " ".join(context.args).strip()
    if not message: return await update.message.reply_text("Contoh: /broadcast Halo semua")
    sent = 0
    for uid in list_user_ids():
        try:
            await context.bot.send_message(chat_id=uid, text=message); sent += 1
        except Exception: logger.exception("Broadcast failed to %s", uid)
    await update.message.reply_text(f"Broadcast terkirim ke {sent} user.")


async def shell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    if not is_admin(update.effective_user.id): return await update.message.reply_text("Khusus admin.")
    await send_long_message(update, run_shell(" ".join(context.args)))


async def sysinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    if not is_admin(update.effective_user.id): return await update.message.reply_text("Khusus admin.")
    await update.message.reply_text(system_info())


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await send_long_message(update, web_search(" ".join(context.args).strip()))


async def asksearch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    query = " ".join(context.args).strip()
    if not query: return await update.message.reply_text("Contoh: /asksearch perkembangan AI terbaru")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await send_long_message(update, agent.respond(update.effective_user.id, f"Ringkas hasil pencarian ini dalam bahasa Indonesia:\n\n{web_search(query)}"))


async def cmd_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(price(" ".join(context.args)))


async def cmd_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await update.message.reply_text(coin_detail(" ".join(context.args)))


async def cmd_trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await send_long_message(update, trending())


async def cmd_newpairs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await send_long_message(update, new_pairs(" ".join(context.args)))


async def cmd_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await send_long_message(update, token_info(" ".join(context.args)))


async def cmd_dex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await send_long_message(update, dex_search(" ".join(context.args)))


async def cmd_gmgn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await update.message.reply_text(gmgn_link(" ".join(context.args)))


async def social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    if len(context.args) < 2: return await update.message.reply_text("Contoh: /social reddit groq api")
    await update.message.reply_text(social_search(context.args[0], " ".join(context.args[1:])))


async def socialprompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update)
    if len(context.args) < 2: return await update.message.reply_text("Contoh: /socialprompt linkedin AI agent untuk bisnis")
    await send_long_message(update, agent.respond(update.effective_user.id, social_prompt(context.args[0], " ".join(context.args[1:]))))


async def platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await update.message.reply_text(platform_guide(" ".join(context.args)))


async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await update.message.reply_text(calculate(" ".join(context.args).strip()))


async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); content = " ".join(context.args).strip()
    if not content: return await update.message.reply_text("Contoh: /note beli paket internet besok")
    add_note(update.effective_user.id, content); await update.message.reply_text("Catatan tersimpan.")


async def notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); rows = list_notes(update.effective_user.id)
    if not rows: return await update.message.reply_text("Belum ada catatan.")
    await send_long_message(update, "\n\n".join(["Catatan terakhir:"] + [f"{i}. {c}\n   {t}" for i, (_, c, t) in enumerate(rows, 1)]))


async def clearnotes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); clear_notes(update.effective_user.id); await update.message.reply_text("Catatan dihapus.")


async def persona(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); value = " ".join(context.args).strip()
    if not value: return await update.message.reply_text(f"Persona: {get_persona(update.effective_user.id) or 'Belum ada.'}")
    set_persona(update.effective_user.id, value); await update.message.reply_text("Persona disimpan.")


async def clearpersona(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); clear_persona(update.effective_user.id); await update.message.reply_text("Persona dihapus.")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); path = None; await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        tg_file = await update.message.photo[-1].get_file()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp: path = tmp.name
        await tg_file.download_to_drive(path)
        prompt = update.message.caption or "Jelaskan isi gambar ini secara detail dalam bahasa Indonesia. Jika ada teks, baca teksnya."
        reply = vision_ai.vision(path, prompt)
    except Exception:
        logger.exception("Failed analyzing image"); reply = "Gagal membaca gambar. Cek GROQ_VISION_MODEL atau logs/bot.log."
    finally:
        if path:
            try: os.remove(path)
            except Exception: pass
    await send_long_message(update, reply)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); path = None; await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        doc = update.message.document; tg_file = await doc.get_file(); suffix = os.path.splitext(doc.file_name or "file.txt")[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp: path = tmp.name
        await tg_file.download_to_drive(path)
        if suffix in [".jpg", ".jpeg", ".png", ".webp"]: reply = vision_ai.vision(path, "Analisis gambar ini dalam bahasa Indonesia. Baca teks jika ada.")
        else: reply = agent.respond(update.effective_user.id, f"Ringkas file ini:\n\n{read_text_file(path)}")
    except Exception:
        logger.exception("Failed reading document"); reply = "Gagal membaca file/gambar."
    finally:
        if path:
            try: os.remove(path)
            except Exception: pass
    await send_long_message(update, reply)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_user(update); await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try: reply = agent.respond(update.effective_user.id, update.message.text)
    except Exception:
        logger.exception("Failed to handle message"); reply = "Maaf, terjadi gangguan. Cek logs/bot.log."
    await send_long_message(update, reply)


def register_handlers(app):
    for name, func in [
        ("start", start), ("help", help_command), ("reset", reset), ("status", status), ("id", user_id),
        ("stats", stats), ("users", users), ("broadcast", broadcast), ("shell", shell), ("sysinfo", sysinfo),
        ("search", search), ("asksearch", asksearch),
        ("price", cmd_price), ("coin", cmd_coin), ("trending", cmd_trending), ("newpairs", cmd_newpairs),
        ("token", cmd_token), ("dex", cmd_dex), ("gmgn", cmd_gmgn),
        ("social", social), ("socialprompt", socialprompt), ("platform", platform),
        ("calc", calc), ("note", note), ("notes", notes), ("clearnotes", clearnotes),
        ("persona", persona), ("clearpersona", clearpersona),
    ]:
        app.add_handler(CommandHandler(name, func))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
