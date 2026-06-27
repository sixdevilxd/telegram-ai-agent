# Telegram AI Agent with Groq

AI agent Telegram berbasis Python, Groq HTTP API, SQLite memory, dan siap jalan di Termux.

## Fitur v5 Over Power

- Auto tool routing: `hitung`, `cari`, `catat`
- `/asksearch` = web search lalu diringkas AI
- File reader untuk `.txt`, `.md`, `.csv`, `.json`, `.py`, `.log`
- Persona mode per user
- Notes pribadi
- Admin dashboard command:
  - `/stats`
  - `/users`
  - `/broadcast pesan`
  - `/shell command` dengan allowlist aman
  - `/sysinfo`
- SQLite user tracking
- Logging dan keep-alive

## Update

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

## Command penting

```text
/asksearch perkembangan AI terbaru
/users
/stats
/shell ls
/sysinfo
/broadcast Halo semua
```

## `.env`

```env
TELEGRAM_BOT_TOKEN=token_dari_botfather
GROQ_API_KEY=api_key_groq_kamu
GROQ_MODEL=llama-3.1-8b-instant
BOT_NAME=Keen Telegram Agent
ADMIN_USER_ID=id_telegram_kamu
DATABASE_PATH=data/memory.db
MAX_HISTORY_MESSAGES=10
```

Ambil ID kamu dengan `/id`, lalu isi `ADMIN_USER_ID`.

## Matikan bot

```bash
tmux kill-session -t telegram-agent
pkill -f keep_alive.sh
pkill -f bot.py
```

Jangan pernah push `.env` ke GitHub.
