#!/data/data/com.termux/files/usr/bin/bash
set -e

pkg update && pkg upgrade -y
pkg install python git tmux -y
pip install -r requirements.txt

echo "Install selesai. Copy .env.example ke .env lalu isi token kamu."
