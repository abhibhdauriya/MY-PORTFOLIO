"""
Database connection and generic CRUD helpers.
All queries are parameterized. No string-formatted SQL anywhere.
Uses Turso (cloud) when TURSO_DATABASE_URL/TURSO_AUTH_TOKEN are set in
st.secrets; otherwise falls back to a local SQLite file (portfolio.db).
"""

import sqlite3
import os
from contextlib import contextmanager
from database.schema import SCHEMA_SQL

try:
    import streamlit as st
    _HAS_ST = True
except ImportError:
    _HAS_ST = False

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "portfolio.db")


def _get_turso_creds():
    """Return (url, token) from st.secrets if configured, else (None, None)."""
    if not _HAS_ST:
        return None, None
    try:
        url = st.secrets.get("TURSO_DATABASE_URL")
        token = st.secrets.get("TURSO_AUTH_TOKEN")
        return url, token
    except Exception:
        return None, None


@contextmanager
def get_conn():
    """Context-managed connection: Turso cloud DB if configured, else local SQLite."""
    url, token = _get_turso_creds()
    if url and token:
        import libsql
        conn = libsql.connect(database=url, auth_token=token)
    else:
        conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _rows_to_dicts(cur, rows):
    """Convert raw cursor rows to list of dicts using cursor.description."""
    if not cur.description:
        return []
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in rows]


def init_db():
    """Create all tables if they do not exist, and seed singleton rows."""
    with get_conn() as conn:
        statements = [s.strip() for s in SCHEMA_SQL.split(";") if s.strip()]
        for stmt in statements:
            conn.execute(stmt)
        conn.execute(
            "INSERT OR IGNORE INTO profile (id, name, headline) VALUES (1, ?, ?)",
            ("Abhishek Singh", "MIS & Automation | Excel | Python | Data Analytics | Web Development"),
        )
        conn.execute("INSERT OR IGNORE INTO site_settings (id) VALUES (1)")


def fetch_all(query: str, params: tuple = ()):
    with get_conn() as conn:
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return _rows_to_dicts(cur, rows)


def fetch_one(query: str, params: tuple = ()):
    with get_conn() as conn:
        cur = conn.execute(query, params)
        row = cur.fetchone()
        if row is None:
            return None
        cols = [d[0] for d in cur.description] if cur.description else []
        return dict(zip(cols, row))


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