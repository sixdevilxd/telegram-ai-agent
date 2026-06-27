# Telegram AI Agent with Groq

AI agent Telegram berbasis Python, Groq HTTP API, SQLite memory, dan siap jalan di Termux.

## Fitur v6 Vision

- Chat AI via Telegram
- Bisa baca/analis gambar dari foto Telegram
- Bisa baca gambar sebagai document `.jpg`, `.jpeg`, `.png`, `.webp`
- Auto tool routing: `hitung`, `cari`, `catat`
- `/asksearch` = web search lalu diringkas AI
- File reader untuk `.txt`, `.md`, `.csv`, `.json`, `.py`, `.log`
- Persona mode per user
- Notes pribadi
- Admin tools: `/stats`, `/users`, `/broadcast`, `/shell`, `/sysinfo`
- SQLite user tracking
- Logging dan keep-alive

## Update ke v6

```bash
cd telegram-ai-agent
git pull
pip install -r requirements.txt
chmod +x scripts/*.sh
```

Edit `.env`, tambahkan model vision:

```env
GROQ_VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
```

Jalankan:

```bash
python bot.py
```

Jika pakai tmux:

```bash
tmux kill-session -t telegram-agent
tmux new -s telegram-agent
bash scripts/keep_alive.sh
```

## `.env` lengkap

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

## Cara pakai gambar

- Kirim foto langsung ke bot
- Bisa pakai caption sebagai instruksi, contoh: `apa isi screenshot ini?`
- Bot akan membaca objek dan teks yang ada di gambar

## Matikan bot

```bash
tmux kill-session -t telegram-agent
pkill -f keep_alive.sh
pkill -f bot.py
```

Jangan pernah push `.env` ke GitHub.
