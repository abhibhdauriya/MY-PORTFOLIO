"""
Handles saving, retrieving, and deleting uploaded files on local disk.
File paths are stored in the DB as relative paths (e.g. "uploads/projects/xyz.png").
"""

import os
import uuid
from utils.validators import get_extension, is_allowed_file, is_file_size_ok, ALLOWED_EXT_ALL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

SUBFOLDERS = ["profile", "projects", "certificates", "resume", "screenshots"]


def ensure_upload_dirs():
    for folder in SUBFOLDERS:
        os.makedirs(os.path.join(UPLOADS_DIR, folder), exist_ok=True)


def save_uploaded_file(uploaded_file, subfolder: str) -> str | None:
    """
    Save a Streamlit UploadedFile object into uploads/<subfolder>/.
    Returns the relative path to store in the DB, or None if validation fails.
    """
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

    return os.path.join("uploads", subfolder, safe_name)


def delete_file(relative_path: str):
    if not relative_path:
        return
    full_path = os.path.join(BASE_DIR, relative_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        try:
            os.remove(full_path)
        except OSError:
            pass


def get_full_path(relative_path: str) -> str:
    return os.path.join(BASE_DIR, relative_path) if relative_path else ""


def file_exists(relative_path: str) -> bool:
    if not relative_path:
        return False
    return os.path.isfile(os.path.join(BASE_DIR, relative_path))
