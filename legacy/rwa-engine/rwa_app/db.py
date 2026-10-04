"""Database plumbing: connection + (re)building the database from SQL files.

Provided complete — you don't need to change this file in Week 1.
"""
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_ROOT / "sql"
DEFAULT_DB_PATH = PROJECT_ROOT / "rwa.db"


def get_connection(db_path: Path | str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row          # rows behave like dicts: row["loan_id"]
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Drop and recreate all tables, then load seed data."""
    for name in ("schema.sql", "seed.sql"):
        conn.executescript((SQL_DIR / name).read_text(encoding="utf-8"))
    conn.commit()
