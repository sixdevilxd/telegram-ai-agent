from config import MAX_HISTORY_MESSAGES
from storage.database import get_connection


def add_message(user_id: int, role: str, content: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
        (str(user_id), role, content),
    )
    conn.commit()
    conn.close()


def get_recent_messages(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT role, content FROM messages
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (str(user_id), MAX_HISTORY_MESSAGES),
    )
    rows = cur.fetchall()
    conn.close()

    rows = list(reversed(rows))
    return [{"role": role, "content": content} for role, content in rows]


def clear_user_memory(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE user_id = ?", (str(user_id),))
    conn.commit()
    conn.close()
