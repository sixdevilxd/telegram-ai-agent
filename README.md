# Telegram AI Agent with Groq

AI agent Telegram berbasis Python, Groq HTTP API, SQLite memory, dan siap jalan di Termux.

## Fitur v3

- Chat AI via Telegram
- Backend Groq tanpa package `groq`, aman untuk Termux
- Memory percakapan per user pakai SQLite
- `/search` web search sederhana
- `/calc` kalkulator aman
- `/note`, `/notes`, `/clearnotes` catatan pribadi
- `/id` untuk ambil Telegram user ID
- `/stats` khusus admin
- Logging ke `logs/bot.log`
- Keep-alive script agar bot restart otomatis jika crash

## Update

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

Ambil ID kamu dengan command Telegram:

```text
/id
```

Lalu masukkan ke `ADMIN_USER_ID`.

## Jalankan 24 Jam

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
- `/reset` - hapus memory chat
- `/status` - cek status bot
- `/id` - lihat Telegram user ID
- `/search berita AI terbaru` - cari info web
- `/calc 25000*3+10000` - kalkulator
- `/note beli paket internet besok` - simpan catatan
- `/notes` - lihat catatan
- `/clearnotes` - hapus catatan
- `/stats` - statistik admin

## Matikan bot

```bash
tmux kill-session -t telegram-agent
pkill -f keep_alive.sh
pkill -f bot.py
```

## Catatan Keamanan

Jangan pernah push file `.env` ke GitHub. Simpan token Telegram dan API key Groq hanya di `.env` lokal.
