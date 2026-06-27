import shlex
import subprocess

# Hanya command dasar ini yang boleh dijalankan.
ALLOWED_BASE = {
    "pwd", "ls", "df", "du", "free", "uptime", "date", "whoami",
    "python", "python3", "pip", "git",
}


def run_shell(command: str) -> str:
    command = command.strip()
    if not command:
        return "Contoh: /shell ls"

    try:
        # Tokenisasi aman; tidak memakai shell=True sehingga injeksi seperti
        # 'ls; cat .env' atau 'ls && rm -rf data/' tidak akan dieksekusi.
        args = shlex.split(command)
    except ValueError as exc:
        return f"Command tidak valid: {exc}"

    if not args:
        return "Command kosong."

    base = args[0]
    if base not in ALLOWED_BASE:
        return (
            "Command tidak diizinkan demi keamanan.\n"
            "Allowed: " + ", ".join(sorted(ALLOWED_BASE))
        )

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=20,
        )
        output = result.stdout or result.stderr or "Tidak ada output."
        return output[:3500]
    except FileNotFoundError:
        return f"Command '{base}' tidak ditemukan."
    except subprocess.TimeoutExpired:
        return "Command timeout (>20 detik)."
    except Exception as exc:
        return f"Shell error: {exc}"
