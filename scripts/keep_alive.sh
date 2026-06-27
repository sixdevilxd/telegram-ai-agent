#!/data/data/com.termux/files/usr/bin/bash
while true; do
  echo "Starting Telegram AI Agent..."
  python bot.py
  echo "Bot stopped. Restarting in 5 seconds..."
  sleep 5
done
