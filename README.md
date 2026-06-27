# Telegram AI Agent with Groq

AI agent Telegram berbasis Python, Groq HTTP API, SQLite memory, dan siap jalan di Termux.

## Fitur v4

- Chat AI via Telegram
- Groq HTTP API tanpa package `groq`, aman untuk Termux
- Memory percakapan per user
- Auto tool routing tanpa command:
  - `hitung 25000*3`
  - `cari berita AI terbaru`
  - `catat ide bisnis bot telegram`
- File reader untuk `.txt`, `.md`, `.csv`, `.json`, `.py`, `.log`
- Persona mode per user
- Notes pribadi
- Kalkulator aman
- Web search sederhana
- Admin stats
- Logging ke `logs/bot.log`
- Keep-alive script

## Update

```bash
cd telegram-ai-agent
git pull
pip install -r requirements.txt
chmod +x scripts/*.sh
python bot.py
```

## Jalankan 24 Jam

```bash
tmux new -s telegram-agent
bash scripts/keep_alive.sh
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

Ambil ID kamu dengan `/id`, lalu masukkan ke `ADMIN_USER_ID`.

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
- `/persona jawab seperti mentor bisnis` - set persona
- `/persona` - lihat persona
- `/clearpersona` - hapus persona
- `/stats` - statistik admin

## Contoh auto tool

```text
hitung 15000*4+2000
cari update terbaru groq api
catat ide konten: tutorial termux bot telegram
```

## Matikan bot

```bash
tmux kill-session -t telegram-agent
pkill -f keep_alive.sh
pkill -f bot.py
```

## Keamanan

Jangan pernah push `.env` ke GitHub.
