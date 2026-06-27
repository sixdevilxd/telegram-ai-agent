from storage.database import get_connection


def add_note(user_id: int, content: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (user_id, content) VALUES (?, ?)",
        (str(user_id), content),
    )
    conn.commit()
    conn.close()


def list_notes(user_id: int, limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, content, created_at FROM notes
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (str(user_id), limit),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def clear_notes(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE user_id = ?", (str(user_id),))
    conn.commit()
    conn.close()


def count_notes() -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM notes")
    total = cur.fetchone()[0]
    conn.close()
    return total
