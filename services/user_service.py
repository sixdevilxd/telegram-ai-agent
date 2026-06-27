from storage.database import get_connection


def upsert_user(user_id: int, username: str = "", first_name: str = ""):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            last_seen = CURRENT_TIMESTAMP
        """,
        (str(user_id), username or "", first_name or ""),
    )
    conn.commit()
    conn.close()


def list_user_ids():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users ORDER BY last_seen DESC")
    rows = cur.fetchall()
    conn.close()
    return [int(row[0]) for row in rows]


def list_users(limit: int = 20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, username, first_name, last_seen FROM users ORDER BY last_seen DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows
