import sqlite3
from pathlib import Path

DB_PATH = Path("data/jobs.db")

_WRITE_KEYWORDS = {"insert", "update", "delete", "drop", "alter", "create", "truncate"}


def get_schema() -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='jobs'")
    schema = cursor.fetchone()[0]
    conn.close()
    return schema


def run_query(sql: str) -> list[dict]:
    first_word = sql.strip().split()[0].lower()
    if first_word in _WRITE_KEYWORDS:
        raise ValueError(f"Query tidak diizinkan: {first_word.upper()}")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()
