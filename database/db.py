"""
Database connection and generic CRUD helpers.
All queries are parameterized. No string-formatted SQL anywhere.
"""

import sqlite3
import os
from contextlib import contextmanager
from database.schema import SCHEMA_SQL

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "portfolio.db")


@contextmanager
def get_conn():
    """Context-managed SQLite connection with row factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Create all tables if they do not exist, and seed singleton rows."""
    with get_conn() as conn:
        conn.executescript(SCHEMA_SQL)
        conn.execute(
            "INSERT OR IGNORE INTO profile (id, name, headline) VALUES (1, ?, ?)",
            ("Abhishek Singh", "MIS & Automation | Excel | Python | Data Analytics | Web Development"),
        )
        conn.execute("INSERT OR IGNORE INTO site_settings (id) VALUES (1)")


def fetch_all(query: str, params: tuple = ()):
    with get_conn() as conn:
        cur = conn.execute(query, params)
        return [dict(row) for row in cur.fetchall()]


def fetch_one(query: str, params: tuple = ()):
    with get_conn() as conn:
        cur = conn.execute(query, params)
        row = cur.fetchone()
        return dict(row) if row else None


def execute(query: str, params: tuple = ()):
    """For INSERT/UPDATE/DELETE. Returns lastrowid."""
    with get_conn() as conn:
        cur = conn.execute(query, params)
        return cur.lastrowid


def insert_row(table: str, data: dict) -> int:
    """Generic insert helper. `data` keys must match column names exactly."""
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    return execute(query, tuple(data.values()))


def update_row(table: str, row_id: int, data: dict):
    """Generic update helper for a single-PK-id table."""
    set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
    execute(query, tuple(data.values()) + (row_id,))


def delete_row(table: str, row_id: int):
    execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
