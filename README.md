# Telegram AI Agent with Groq

AI agent Telegram berbasis Python, Groq HTTP API, SQLite memory, Termux, vision, dan social intelligence.

## Fitur v7 Social Intelligence

- Mengenal platform: X/Twitter, LinkedIn, Reddit, Facebook, Instagram, TikTok, YouTube
- `/social platform query` untuk membuat link pencarian sosial
- `/socialprompt platform topik` untuk membuat konten siap posting
- `/platform nama` untuk panduan strategi tiap platform
- Auto routing: `cari di reddit groq api`, `cari di linkedin ai agent`
- Vision: baca/analis gambar Telegram
- File reader: `.txt`, `.md`, `.csv`, `.json`, `.py`, `.log`
- Admin tools: `/stats`, `/users`, `/broadcast`, `/shell`, `/sysinfo`

## Update ke v7

```bash
cd telegram-ai-agent
git pull
pip install -r requirements.txt
chmod +x scripts/*.sh
python bot.py
```

Jika pakai tmux:

```bash
tmux kill-session -t telegram-agent
tmux new -s telegram-agent
bash scripts/keep_alive.sh
```

## Contoh Sosmed

```text
/social reddit groq api
/social linkedin ai agent untuk bisnis
/social twitter openai groq comparison
/socialprompt linkedin AI agent untuk UMKM
/socialprompt reddit pengalaman pakai Termux bot
/platform linkedin
/platform reddit
```

## `.env`

```env
TELEGRAM_BOT_TOKEN=token_dari_botfather
GROQ_API_KEY=api_key_groq_kamu
GROQ_MODEL=llama-3.1-8b-instant
GROQ_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
BOT_NAME=Keen Telegram Agent
ADMIN_USER_ID=id_telegram_kamu
DATABASE_PATH=data/memory.db
MAX_HISTORY_MESSAGES=10
```

Jangan pernah push `.env` ke GitHub.
