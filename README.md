# Telegram AI Agent with Groq

AI agent Telegram berbasis Python, Groq HTTP API, SQLite memory, Termux, vision, social intelligence, dan crypto real-time.

## Fitur v8 Crypto Intelligence

- Data crypto real-time gratis:
  - CoinGecko: harga, market cap, volume, trending semua koin
  - DexScreener: new pairs, new launch, info token lintas DEX/chain
- Command crypto:
  - `/price bitcoin`
  - `/coin pepe`
  - `/trending`
  - `/newpairs solana`
  - `/token <kontrak>`
  - `/dex pepe`
  - `/gmgn <kontrak>` (quick link gmgn/birdeye)
- Optional Birdeye via `BIRDEYE_API_KEY`
- Social intelligence: X/Twitter, LinkedIn, Reddit, Facebook, Instagram, TikTok, YouTube
- Vision: baca/analis gambar
- File reader, persona, notes, admin tools, web search

## Update ke v8

```bash
cd telegram-ai-agent
git pull
pip install -r requirements.txt
python bot.py
```

Jika pakai tmux:

```bash
tmux kill-session -t telegram-agent
tmux new -s telegram-agent
bash scripts/keep_alive.sh
```

## Contoh Crypto

```text
/price bitcoin
/price solana
/trending
/newpairs solana
/newpairs ethereum
/dex pepe
/token EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
/gmgn EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

Auto:

```text
harga bitcoin
harga solana
new pairs solana
cek token <kontrak>
```

## Sumber Data

- CoinGecko dan DexScreener: gratis, real-time, tanpa API key
- Birdeye: butuh `BIRDEYE_API_KEY` (opsional, berbayar)
- GMGN/fomo: tidak ada API publik resmi, bot memberikan quick link

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
BIRDEYE_API_KEY=
```

Jangan pernah push `.env` ke GitHub.
