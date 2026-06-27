import platform
import sys


def system_info() -> str:
    return (
        "System info:\n"
        f"- Python: {sys.version.split()[0]}\n"
        f"- Platform: {platform.platform()}\n"
        f"- Machine: {platform.machine()}"
    )
