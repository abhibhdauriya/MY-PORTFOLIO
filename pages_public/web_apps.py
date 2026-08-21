import streamlit as st
from database.db import fetch_all
from components.navbar import render_page_title, render_footer
from components.cards import project_card, empty_state
from utils.helpers import record_page_view


def render():
    record_page_view("web_apps")
    render_page_title("Applications", "Web Applications", "Streamlit apps, dashboards, and data tools I've built and deployed.")

    projects = fetch_all(
        "SELECT * FROM projects WHERE is_published = 1 AND category = 'Web Development' ORDER BY created_at DESC"
    )

    if not projects:
        empty_state("Web applications will appear here once added in the admin panel.")
    else:
        for project in projects:
            project_card(project, on_details=lambda pid: (st.session_state.update(selected_project_id=pid), st.switch_page("pages_public/projects.py")))

    render_footer()

render()
