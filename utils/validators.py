"""
Validation helpers for forms and file uploads.
"""

import re
from urllib.parse import urlparse

URL_PATTERN = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "webp"}
ALLOWED_DOC_EXT = {"pdf"}
ALLOWED_EXCEL_EXT = {"xlsx", "xlsm", "xls", "csv"}
ALLOWED_EXT_ALL = ALLOWED_IMAGE_EXT | ALLOWED_DOC_EXT | ALLOWED_EXCEL_EXT

MAX_FILE_SIZE_MB = 10


def is_valid_url(url: str) -> bool:
    if not url:
        return True  # empty/optional fields are fine
    if not URL_PATTERN.match(url):
        return False
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme in ("http", "https") and parsed.netloc)
    except ValueError:
        return False


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    return bool(EMAIL_PATTERN.match(email))


def get_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def is_allowed_file(filename: str, allowed: set) -> bool:
    return get_extension(filename) in allowed


def is_file_size_ok(file_bytes: bytes, max_mb: int = MAX_FILE_SIZE_MB) -> bool:
    return len(file_bytes) <= max_mb * 1024 * 1024


def required_field_ok(value: str) -> bool:
    return bool(value and value.strip())
