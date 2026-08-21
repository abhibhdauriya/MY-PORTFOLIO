"""
Database backup and data export utilities.
"""

import json
import io
import csv
from datetime import datetime
from database.db import DB_PATH, fetch_all


def get_db_file_bytes() -> bytes:
    """Return raw SQLite file bytes for download as a backup."""
    with open(DB_PATH, "rb") as f:
        return f.read()


def backup_filename() -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"portfolio_backup_{stamp}.db"


EXPORT_TABLES = [
    "profile", "projects", "skills", "experience",
    "certificates", "links", "site_settings",
]


def export_all_json() -> bytes:
    """Export all portfolio content tables as a single JSON blob."""
    data = {table: fetch_all(f"SELECT * FROM {table}") for table in EXPORT_TABLES}
    return json.dumps(data, indent=2, default=str).encode("utf-8")


def export_table_csv(table: str) -> bytes:
    """Export a single table as CSV bytes."""
    rows = fetch_all(f"SELECT * FROM {table}")
    buf = io.StringIO()
    if rows:
        writer = csv.DictWriter(buf, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return buf.getvalue().encode("utf-8")
