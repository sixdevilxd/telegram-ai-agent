# Telegram AI Agent with Groq

AI agent Telegram berbasis Python, Groq HTTP API, SQLite memory, dan siap jalan di Termux.

## Fitur

- Chat AI via Telegram
- Backend LLM Groq tanpa package `groq`, jadi lebih aman untuk Termux
- Memory percakapan per user pakai SQLite
- Command `/start`, `/help`, `/reset`, `/status`
- Siap deploy di Termux
- Aman untuk GitHub karena `.env` tidak dipush

## Install di Termux

```bash
pkg update && pkg upgrade -y
pkg install python git -y

git clone https://github.com/sixdevilxd/telegram-ai-agent.git
cd telegram-ai-agent

pip install -r requirements.txt
cp .env.example .env
nano .env
python bot.py
```

## Kalau sebelumnya install gagal di package groq

Update repo dan install ulang:

```bash
cd telegram-ai-agent
git pull
pip uninstall groq pydantic pydantic-core -y
pip install -r requirements.txt
python bot.py
```

## Isi `.env`

```env
TELEGRAM_BOT_TOKEN=token_dari_botfather
GROQ_API_KEY=api_key_groq_kamu
GROQ_MODEL=llama-3.1-8b-instant
BOT_NAME=Keen Telegram Agent
ADMIN_USER_ID=id_telegram_kamu
```

## Jalankan 24 Jam di Termux

```bash
pkg install tmux -y
tmux new -s telegram-agent
python bot.py
```

Keluar tanpa mematikan bot:

```text
CTRL + B lalu D
```

Masuk lagi:

```bash
tmux attach -t telegram-agent
```

## Catatan Keamanan

Jangan pernah push file `.env` ke GitHub. Simpan token Telegram dan API key Groq hanya di `.env` lokal.
