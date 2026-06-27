import subprocess

SAFE_COMMANDS = [
    "pwd", "ls", "df", "du", "free", "uptime", "date", "whoami",
    "python --version", "pip list", "git status", "git log --oneline -5",
]


def run_shell(command: str) -> str:
    command = command.strip()
    if not command:
        return "Contoh: /shell ls"

    allowed = any(command == c or command.startswith(c + " ") for c in SAFE_COMMANDS)
    if not allowed:
        return (
            "Command tidak diizinkan demi keamanan.\n"
            "Allowed: pwd, ls, df, du, free, uptime, date, whoami, python --version, pip list, git status"
        )

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        output = result.stdout or result.stderr or "Tidak ada output."
        return output[:3500]
    except Exception as exc:
        return f"Shell error: {exc}"
