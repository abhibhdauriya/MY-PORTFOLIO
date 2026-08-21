import streamlit as st
from database.db import fetch_all
from components.navbar import render_page_title, render_footer
from components.cards import project_card, empty_state
from utils.helpers import record_page_view

EXCEL_CATEGORIES = ("Excel Automation", "VBA")


def render():
    record_page_view("excel")
    render_page_title(
        "Automation",
        "Excel & VBA Automation",
        "Professional Excel automation projects — MIS reporting, VBA macros, Power Query pipelines. All sample files are sanitized demo data.",
    )

    placeholders = ",".join("?" * len(EXCEL_CATEGORIES))
    projects = fetch_all(
        f"SELECT * FROM projects WHERE is_published = 1 AND category IN ({placeholders}) ORDER BY created_at DESC",
        EXCEL_CATEGORIES,
    )

    if not projects:
        empty_state("Excel & VBA projects will appear here once added in the admin panel.")
    else:
        for project in projects:
            project_card(project, on_details=lambda pid: (st.session_state.update(selected_project_id=pid), st.switch_page("pages_public/projects.py")))

    render_footer()

render()
