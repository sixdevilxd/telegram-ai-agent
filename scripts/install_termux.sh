#!/data/data/com.termux/files/usr/bin/bash
set -e

pkg update && pkg upgrade -y

# Paket inti
pkg install python git tmux termux-api -y

# Perbaiki SSL (mencegah error saat web search / crypto API)
pkg install ca-certificates openssl -y

# Dependency untuk Pillow (analisa chart / baca gambar)
pkg install libjpeg-turbo libpng freetype -y

pip install -r requirements.txt

echo "Install selesai. Copy .env.example ke .env lalu isi token kamu."
echo "Tips: jalankan 'termux-wake-lock' atau pakai scripts/keep_alive.sh agar bot tidak mati saat layar terkunci."
