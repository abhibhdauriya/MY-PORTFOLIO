"""
Reusable UI card components for projects, certificates, links, experience.
"""

import streamlit as st
from utils.helpers import csv_to_list, STATUS_COLORS, truncate
from utils.file_manager import file_exists, get_full_path


def status_badge(status: str):
    color = STATUS_COLORS.get(status, "#6b7280")
    st.markdown(
        f'<span class="pf-badge" style="background:{color}">{status}</span>',
        unsafe_allow_html=True,
    )


def render_tags(tags_csv: str):
    tags = csv_to_list(tags_csv)
    if not tags:
        return
    html = "".join([f'<span class="pf-tag">{t}</span>' for t in tags])
    st.markdown(html, unsafe_allow_html=True)


def project_card(project: dict, on_details=None):
    """Renders a single project as a professional card with action buttons."""
    with st.container():
        st.markdown('<div class="pf-card">', unsafe_allow_html=True)

        col_img, col_body = st.columns([1, 2.6]) if project.get("thumbnail_path") and file_exists(project["thumbnail_path"]) else (None, st.container())

        if col_img is not None:
            with col_img:
                st.image(get_full_path(project["thumbnail_path"]), use_container_width=True)
            body = col_body
        else:
            body = col_body

        with body:
            top = st.columns([3, 1])
            with top[0]:
                st.markdown(f'<div class="pf-card-title">{project["title"]}</div>', unsafe_allow_html=True)
            with top[1]:
                status_badge(project.get("status", "Completed"))

            st.markdown(
                f'<div class="pf-card-desc">{truncate(project.get("short_description", ""), 160)}</div>',
                unsafe_allow_html=True,
            )
            render_tags(project.get("technologies", ""))

            btn_cols = st.columns(3)
            if project.get("live_url"):
                with btn_cols[0]:
                    st.link_button("Live Demo", project["live_url"], use_container_width=True)
            if project.get("github_url"):
                with btn_cols[1]:
                    st.link_button("GitHub", project["github_url"], use_container_width=True)
            with btn_cols[2]:
                if st.button("Details →", key=f"details_{project['id']}", use_container_width=True):
                    if on_details:
                        on_details(project["id"])

        st.markdown("</div>", unsafe_allow_html=True)


def certificate_card(cert: dict):
    with st.container():
        st.markdown('<div class="pf-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="pf-card-title">{cert["title"]}</div>', unsafe_allow_html=True)
        meta = " • ".join(filter(None, [cert.get("issuing_org", ""), cert.get("issue_date", "")]))
        if meta:
            st.markdown(f'<div class="pf-card-desc">{meta}</div>', unsafe_allow_html=True)
        if cert.get("description"):
            st.markdown(f'<div class="pf-card-desc">{cert["description"]}</div>', unsafe_allow_html=True)
        if cert.get("credential_url"):
            st.link_button("View Credential", cert["credential_url"])
        st.markdown("</div>", unsafe_allow_html=True)


def experience_card(exp: dict):
    with st.container():
        st.markdown('<div class="pf-card">', unsafe_allow_html=True)
        date_range = f'{exp.get("start_date", "")} — {"Present" if exp.get("is_current") else exp.get("end_date", "")}'
        st.markdown(f'<div class="pf-card-title">{exp["position"]} · {exp["company"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pf-card-desc">{date_range}' + (f' · {exp["location"]}' if exp.get("location") else '') + '</div>', unsafe_allow_html=True)
        if exp.get("description"):
            st.markdown(f'<div class="pf-card-desc">{exp["description"]}</div>', unsafe_allow_html=True)
        render_tags(exp.get("technologies", ""))
        st.markdown("</div>", unsafe_allow_html=True)


def empty_state(message: str):
    st.markdown(f'<div class="pf-empty">{message}</div>', unsafe_allow_html=True)
