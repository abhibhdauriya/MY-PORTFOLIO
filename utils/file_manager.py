"""
Handles saving, retrieving, and deleting uploaded files.
Files are saved to local disk AND backed up as bytes in the database
(file_store table) so they survive Streamlit Cloud's ephemeral storage.
If a file is missing on disk (e.g. after a restart), it is automatically
restored from the database before being served.
"""
import os
import uuid
from utils.validators import get_extension, is_allowed_file, is_file_size_ok, ALLOWED_EXT_ALL
from database.db import get_conn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
SUBFOLDERS = ["profile", "projects", "certificates", "resume", "screenshots"]


def _ensure_file_store_table():
    with get_conn() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS file_store (path TEXT PRIMARY KEY, data BLOB, created_at TEXT DEFAULT (datetime('now')))"
        )


def ensure_upload_dirs():
    for folder in SUBFOLDERS:
        os.makedirs(os.path.join(UPLOADS_DIR, folder), exist_ok=True)


def save_uploaded_file(uploaded_file, subfolder: str) -> str | None:
    if uploaded_file is None:
        return None
    filename = uploaded_file.name
    if not is_allowed_file(filename, ALLOWED_EXT_ALL):
        return None
    file_bytes = uploaded_file.getvalue()
    if not is_file_size_ok(file_bytes):
        return None
    ext = get_extension(filename)
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    ensure_upload_dirs()
    folder_path = os.path.join(UPLOADS_DIR, subfolder)
    os.makedirs(folder_path, exist_ok=True)
    full_path = os.path.join(folder_path, safe_name)
    with open(full_path, "wb") as f:
        f.write(file_bytes)

    relative_path = os.path.join("uploads", subfolder, safe_name)

    try:
        _ensure_file_store_table()
        with get_conn() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO file_store (path, data) VALUES (?, ?)",
                (relative_path, file_bytes),
            )
    except Exception:
        pass  # local file still works even if the backup fails

    return relative_path


def _restore_from_backup(relative_path: str) -> bool:
    try:
        with get_conn() as conn:
            cur = conn.execute("SELECT data FROM file_store WHERE path = ?", (relative_path,))
            row = cur.fetchone()
        if not row or row[0] is None:
            return False
        full_path = os.path.join(BASE_DIR, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(row[0])
        return True
    except Exception:
        return False


def delete_file(relative_path: str):
    if not relative_path:
        return
    full_path = os.path.join(BASE_DIR, relative_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            os.remove(full_path)
        except OSError:
            pass
    try:
        with get_conn() as conn:
            conn.execute("DELETE FROM file_store WHERE path = ?", (relative_path,))
    except Exception:
        pass


def get_full_path(relative_path: str) -> str:
    if relative_path and not os.path.isfile(os.path.join(BASE_DIR, relative_path)):
        _restore_from_backup(relative_path)
    return os.path.join(BASE_DIR, relative_path) if relative_path else ""


def file_exists(relative_path: str) -> bool:
    if not relative_path:
        return False
    full_path = os.path.join(BASE_DIR, relative_path)
    if os.path.isfile(full_path):
        return True
    return _restore_from_backup(relative_path)
