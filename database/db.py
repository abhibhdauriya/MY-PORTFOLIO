"""
Database connection and generic CRUD helpers.
Uses Turso's embedded-replica mode: a local synced copy for fast reads,
with writes pushed to the remote Turso DB via periodic sync. Falls back
to a plain local SQLite file if Turso secrets aren't configured.
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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "portfolio.db")
REPLICA_PATH = os.path.join(BASE_DIR, "local_replica.db")


def _get_turso_creds():
    if not _HAS_ST:
        return None, None
    try:
        url = st.secrets.get("TURSO_DATABASE_URL")
        token = st.secrets.get("TURSO_AUTH_TOKEN")
        return url, token
    except Exception:
        return None, None


def _build_conn():
    url, token = _get_turso_creds()
    if url and token:
        import libsql
        conn = libsql.connect(REPLICA_PATH, sync_url=url, auth_token=token)
        conn.sync()
        return conn
    else:
        return sqlite3.connect(DB_PATH, check_same_thread=False)


if _HAS_ST:
    _cached_conn = st.cache_resource(_build_conn)
else:
    def _cached_conn():
        return _build_conn()


@contextmanager
def get_conn():
    conn = _cached_conn()
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
        if hasattr(conn, "sync"):
            conn.sync()
    except Exception:
        conn.rollback()
        raise


def _rows_to_dicts(cur, rows):
    if not cur.description:
        return []
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in rows]


def init_db():
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
    with get_conn() as conn:
        cur = conn.execute(query, params)
        return cur.lastrowid


def insert_row(table: str, data: dict) -> int:
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    return execute(query, tuple(data.values()))


def update_row(table: str, row_id: int, data: dict):
    set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
    execute(query, tuple(data.values()) + (row_id,))


def delete_row(table: str, row_id: int):
    execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
