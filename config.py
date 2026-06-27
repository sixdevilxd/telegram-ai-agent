import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
BOT_NAME = os.getenv("BOT_NAME", "Keen Telegram Agent")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID", "")
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/memory.db")
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))
