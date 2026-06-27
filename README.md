# Telegram AI Agent with Groq

AI agent Telegram berbasis Python, Groq HTTP API, SQLite memory, dan siap jalan di Termux.

## Fitur v2

- Chat AI via Telegram
- Backend LLM Groq tanpa package `groq`, aman untuk Termux
- Memory percakapan per user pakai SQLite
- Command `/start`, `/help`, `/reset`, `/status`
- Web search sederhana via `/search kata kunci`
- Admin stats via `/stats`
- Logging ke `logs/bot.log`
- Keep-alive script agar bot restart otomatis jika crash

## Update dari v1 ke v2

```bash
cd telegram-ai-agent
git pull
pip install -r requirements.txt
chmod +x scripts/*.sh
python bot.py
```

## Install awal di Termux

```bash
pkg update && pkg upgrade -y
pkg install python git tmux -y

git clone https://github.com/sixdevilxd/telegram-ai-agent.git
cd telegram-ai-agent

pip install -r requirements.txt
cp .env.example .env
nano .env
python bot.py
```

## Isi `.env`

```env
TELEGRAM_BOT_TOKEN=token_dari_botfather
GROQ_API_KEY=api_key_groq_kamu
GROQ_MODEL=llama-3.1-8b-instant
BOT_NAME=Keen Telegram Agent
ADMIN_USER_ID=id_telegram_kamu
DATABASE_PATH=data/memory.db
MAX_HISTORY_MESSAGES=10
```

## Jalankan 24 Jam di Termux

```bash
tmux new -s telegram-agent
bash scripts/keep_alive.sh
```

Keluar tanpa mematikan bot:

```text
CTRL + B lalu D
```

Masuk lagi:

```bash
tmux attach -t telegram-agent
```

## Command

- `/start` - mulai bot
- `/help` - bantuan
- `/reset` - hapus memory kamu
- `/status` - cek status bot
- `/search berita AI terbaru` - cari info web
- `/stats` - statistik khusus admin

## Catatan Keamanan

Jangan pernah push file `.env` ke GitHub. Simpan token Telegram dan API key Groq hanya di `.env` lokal.
