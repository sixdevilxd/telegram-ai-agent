from storage.database import get_connection


def set_persona(user_id: int, persona: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO personas (user_id, persona) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET persona = excluded.persona
        """,
        (str(user_id), persona),
    )
    conn.commit()
    conn.close()


def get_persona(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT persona FROM personas WHERE user_id = ?", (str(user_id),))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""


def clear_persona(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM personas WHERE user_id = ?", (str(user_id),))
    conn.commit()
    conn.close()
