import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Provider LLM: "groq" (default), "openrouter", atau "agentrouter"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").strip().lower()

# --- Groq ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_VISION_MODEL = os.getenv("GROQ_VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

# --- OpenRouter (OpenAI-compatible, akses Claude/GPT/Llama/dll) ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4.5")
OPENROUTER_VISION_MODEL = os.getenv("OPENROUTER_VISION_MODEL", "")

# --- Agentrouter (OpenAI-compatible) ---
AGENTROUTER_API_KEY = os.getenv("AGENTROUTER_API_KEY", "")
AGENTROUTER_BASE_URL = os.getenv("AGENTROUTER_BASE_URL", "https://agentrouter.org/v1/chat/completions")
AGENTROUTER_MODEL = os.getenv("AGENTROUTER_MODEL", "claude-opus-4-8")


BOT_NAME = os.getenv("BOT_NAME", "Keen Telegram Agent")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID", "")
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/memory.db")
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))
