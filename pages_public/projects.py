import streamlit as st
from database.db import fetch_all, fetch_one
from components.navbar import render_page_title, render_footer
from components.cards import project_card, empty_state, status_badge, render_tags
from components.filters import project_filters
from utils.helpers import record_page_view, lines_to_list, paginate
from utils.file_manager import file_exists, get_full_path


def render_case_study(project: dict):
    if st.button("← Back to all projects"):
        st.session_state.pop("selected_project_id", None)
        st.rerun()

    st.markdown(f'<div class="hero-title" style="font-size:2rem;">{project["title"]}</div>', unsafe_allow_html=True)
    status_badge(project.get("status", "Completed"))
    st.write("")
    render_tags(project.get("technologies", ""))
    st.write("")

    if project.get("thumbnail_path") and file_exists(project["thumbnail_path"]):
        st.image(get_full_path(project["thumbnail_path"]), use_container_width=True)

    links = st.columns(4)
    if project.get("live_url"):
        with links[0]:
            st.link_button("Live Demo", project["live_url"], use_container_width=True)
    if project.get("github_url"):
        with links[1]:
            st.link_button("GitHub", project["github_url"], use_container_width=True)
    if project.get("documentation_url"):
        with links[2]:
            st.link_button("Documentation", project["documentation_url"], use_container_width=True)
    if project.get("demo_video_url"):
        with links[3]:
            st.link_button("Demo Video", project["demo_video_url"], use_container_width=True)

    st.write("")

    for label, field in [
        ("Problem", "problem"), ("Approach", "approach"), ("Solution", "solution"),
    ]:
        if project.get(field):
            st.markdown(f"### {label}")
            st.markdown(project[field])

    features = lines_to_list(project.get("features", ""))
    if features:
        st.markdown("### Key Features")
        for f in features:
            st.markdown(f"- {f}")

    if project.get("results"):
        st.markdown("### Results")
        st.markdown(project["results"])

    # Downloadable samples (Excel/VBA projects)
    sample_cols = st.columns(3)
    file_fields = [
        ("sample_xlsx_path", "Download Sample (.xlsx)"),
        ("sample_xlsm_path", "Download Sample (.xlsm)"),
        ("pdf_doc_path", "Download Documentation (PDF)"),
    ]
    for i, (field, label) in enumerate(file_fields):
        path = project.get(field)
        if path and file_exists(path):
            with sample_cols[i]:
                with open(get_full_path(path), "rb") as f:
                    st.download_button(label, f, file_name=path.split("/")[-1], use_container_width=True)


def render():
    record_page_view("projects")

    selected_id = st.session_state.get("selected_project_id")
    if selected_id:
        project = fetch_one("SELECT * FROM projects WHERE id = ? AND is_published = 1", (selected_id,))
        if project:
            render_case_study(project)
            render_footer()
            return

    render_page_title("Portfolio", "Projects")

    all_projects = fetch_all("SELECT * FROM projects WHERE is_published = 1 ORDER BY created_at DESC")
    filtered = project_filters(all_projects)

    st.write("")
    if not filtered:
        empty_state("No projects match your search/filter.")
    else:
        page_num = st.session_state.get("projects_page", 1)
        page_items, total_pages = paginate(filtered, page_num, page_size=6)

        for project in page_items:
            project_card(project, on_details=lambda pid: (st.session_state.update(selected_project_id=pid), st.rerun()))

        if total_pages > 1:
            st.write("")
            nav_cols = st.columns([1, 2, 1])
            with nav_cols[0]:
                if page_num > 1 and st.button("← Previous", use_container_width=True):
                    st.session_state["projects_page"] = page_num - 1
                    st.rerun()
            with nav_cols[1]:
                st.markdown(f'<div style="text-align:center; color:#9aa1b5; padding-top:8px;">Page {page_num} of {total_pages}</div>', unsafe_allow_html=True)
            with nav_cols[2]:
                if page_num < total_pages and st.button("Next →", use_container_width=True):
                    st.session_state["projects_page"] = page_num + 1
                    st.rerun()

    render_footer()

render()
