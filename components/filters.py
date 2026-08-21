"""
Search and filter widgets for the projects listing page.
"""

import streamlit as st
from utils.helpers import PROJECT_CATEGORIES


def project_filters(projects: list) -> list:
    """Renders search + filter widgets and returns the filtered project list."""
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        query = st.text_input("Search projects", placeholder="Search by title, tech, tag...", label_visibility="collapsed")
    with col2:
        category = st.selectbox("Category", ["All"] + PROJECT_CATEGORIES, label_visibility="collapsed")
    with col3:
        featured_only = st.checkbox("Featured only")

    filtered = projects
    if query:
        q = query.lower()
        filtered = [
            p for p in filtered
            if q in p["title"].lower()
            or q in (p.get("technologies") or "").lower()
            or q in (p.get("tags") or "").lower()
            or q in (p.get("short_description") or "").lower()
        ]
    if category != "All":
        filtered = [p for p in filtered if p.get("category") == category]
    if featured_only:
        filtered = [p for p in filtered if p.get("is_featured")]

    return filtered
