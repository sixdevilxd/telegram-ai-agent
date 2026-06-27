#!/data/data/com.termux/files/usr/bin/bash
# Cegah Android menidurkan Termux saat layar terkunci (butuh: pkg install termux-api).
termux-wake-lock 2>/dev/null || true

cleanup() {
  echo "Melepas wake-lock..."
  termux-wake-unlock 2>/dev/null || true
  exit 0
}
trap cleanup INT TERM

while true; do
  echo "Starting Telegram AI Agent..."
  python bot.py
  echo "Bot stopped. Restarting in 5 seconds..."
  sleep 5
done
