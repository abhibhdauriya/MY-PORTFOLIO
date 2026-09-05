"""
Database connection and generic CRUD helpers.
Uses Turso's embedded-replica mode: a local synced copy for fast reads,
with writes pushed to the remote Turso DB via periodic sync.

FIX (vs previous version):
1. conn.sync() no longer runs after every read (fetch_one/fetch_all) —
   only after writes (execute/insert_row/update_row/delete_row). This
   removes several unnecessary network round-trips per page load.
2. Both the initial connect+sync AND write-time sync are wrapped in a
   hard timeout. If Turso is unreachable / slow / misconfigured, the
   app falls back to local sqlite instead of hanging forever with an
   infinite "running" spinner and no visible error.
"""
import sqlite3
import os
import logging
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from database.schema import SCHEMA_SQL

try:
    import streamlit as st
    _HAS_ST = True
except ImportError:
    _HAS_ST = False

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "portfolio.db")
REPLICA_PATH = os.path.join(BASE_DIR, "local_replica.db")

# Any single network op (connect+sync, or a write-sync) gets at most this long.
NETWORK_TIMEOUT_SECONDS = 8

_executor = ThreadPoolExecutor(max_workers=2)


def _run_with_timeout(fn, *args, timeout=NETWORK_TIMEOUT_SECONDS, **kwargs):
    """Runs fn in a worker thread and raises TimeoutError if it takes too long.
    Note: the underlying thread may keep running in the background (Python has
    no clean way to kill a thread), but the caller gets control back so the
    app doesn't hang."""
    future = _executor.submit(fn, *args, **kwargs)
    return future.result(timeout=timeout)


def _get_turso_creds():
    if not _HAS_ST:
        return None, None
    try:
        url = st.secrets.get("TURSO_DATABASE_URL")
        token = st.secrets.get("TURSO_AUTH_TOKEN")
        return url, token
    except Exception:
        return None, None


def _connect_turso(url, token):
    import libsql
    conn = libsql.connect(REPLICA_PATH, sync_url=url, auth_token=token)
    conn.sync()
    return conn


def _build_conn():
    url, token = _get_turso_creds()
    if url and token:
        try:
            return _run_with_timeout(_connect_turso, url, token)
        except (FutureTimeoutError, Exception) as e:
            logger.warning(f"Turso connect/sync failed or timed out, falling back to local sqlite: {e}")
            return sqlite3.connect(DB_PATH, check_same_thread=False)
    else:
        return sqlite3.connect(DB_PATH, check_same_thread=False)


if _HAS_ST:
    _cached_conn = st.cache_resource(_build_conn)
else:
    _conn_singleton = None
    def _cached_conn():
        global _conn_singleton
        if _conn_singleton is None:
            _conn_singleton = _build_conn()
        return _conn_singleton


def _safe_sync(conn):
    """Best-effort sync with a timeout. Never raises — a failed/slow sync
    should not break the request, since the local replica already has the
    committed write."""
    if not hasattr(conn, "sync"):
        return
    try:
        _run_with_timeout(conn.sync, timeout=NETWORK_TIMEOUT_SECONDS)
    except (FutureTimeoutError, Exception) as e:
        logger.warning(f"Turso sync after write failed or timed out (data is safe locally): {e}")


@contextmanager
def get_conn(readonly: bool = False):
    """
    readonly=True (used by fetch_one/fetch_all): no sync — local replica
    reads are fast and don't need a network round-trip every time.
    readonly=False (used by execute/insert/update/delete): commits, then
    best-effort syncs to push the write to Turso, with a timeout guard.
    """
    conn = _cached_conn()
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        if not readonly:
            conn.commit()
            _safe_sync(conn)
    except Exception:
        conn.rollback()
        raise


def _rows_to_dicts(cur, rows):
    if not cur.description:
        return []
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in rows]


def init_db():
    with get_conn(readonly=False) as conn:
        statements = [s.strip() for s in SCHEMA_SQL.split(";") if s.strip()]
        for stmt in statements:
            conn.execute(stmt)
        conn.execute(
            "INSERT OR IGNORE INTO profile (id, name, headline) VALUES (1, ?, ?)",
            ("Abhishek Singh", "MIS & Automation | Excel | Python | Data Analytics | Web Development"),
        )
        conn.execute("INSERT OR IGNORE INTO site_settings (id) VALUES (1)")


def fetch_all(query: str, params: tuple = ()):
    with get_conn(readonly=True) as conn:
        cur = conn.execute(query, params)
        rows = cur.fetchall()
        return _rows_to_dicts(cur, rows)


def fetch_one(query: str, params: tuple = ()):
    with get_conn(readonly=True) as conn:
        cur = conn.execute(query, params)
        row = cur.fetchone()
        if row is None:
            return None
        cols = [d[0] for d in cur.description] if cur.description else []
        return dict(zip(cols, row))


def execute(query: str, params: tuple = ()):
    with get_conn(readonly=False) as conn:
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
