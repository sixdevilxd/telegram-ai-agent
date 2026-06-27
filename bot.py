import os

from telegram.ext import ApplicationBuilder

from app.handlers import register_handlers
from config import TELEGRAM_BOT_TOKEN
from core.logging_config import setup_logging
from storage.database import init_db


def main():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    setup_logging()

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN belum diisi di file .env")

    init_db()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    register_handlers(app)

    print("Telegram AI Agent aktif...")
    app.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()
