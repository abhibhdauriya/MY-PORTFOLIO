"""
Small shared helpers used across pages/admin.
"""

from datetime import datetime

PROJECT_CATEGORIES = [
    "MIS", "Excel Automation", "VBA", "Python",
    "Web Development", "Data Analytics", "Dashboard", "Other",
]

PROJECT_STATUSES = ["Planning", "In Development", "Completed", "Live", "Archived"]

SKILL_CATEGORIES = ["Excel", "Programming", "Web", "Data", "Tools"]

STATUS_COLORS = {
    "Planning": "#94a3b8",
    "In Development": "#f59e0b",
    "Completed": "#22c55e",
    "Live": "#3b82f6",
    "Archived": "#6b7280",
}


def csv_to_list(value: str) -> list:
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]


def list_to_csv(items: list) -> str:
    return ", ".join(items)


def lines_to_list(value: str) -> list:
    if not value:
        return []
    return [line.strip() for line in value.split("\n") if line.strip()]


def format_date(date_str: str) -> str:
    if not date_str:
        return ""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %Y")
    except ValueError:
        return date_str


def truncate(text: str, length: int = 140) -> str:
    if not text:
        return ""
    return text if len(text) <= length else text[:length].rsplit(" ", 1)[0] + "..."


def paginate(items: list, page: int, page_size: int = 6) -> tuple[list, int]:
    """Returns (page_items, total_pages) for a list. page is 1-indexed."""
    total_pages = max(1, (len(items) + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    return items[start:start + page_size], total_pages


def record_page_view(page_name: str, project_id: int | None = None):
    """Lightweight, privacy-respecting visit counter. No PII stored."""
    from database.db import insert_row
    try:
        insert_row("page_views", {"page_name": page_name, "project_id": project_id})
    except Exception:
        pass  # analytics should never break the page
