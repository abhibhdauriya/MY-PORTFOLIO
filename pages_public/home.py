"""
Public Home page — hero, featured projects, skills strip, experience preview, contact links.
"""

import streamlit as st
from database.db import fetch_one, fetch_all
from components.cards import project_card, empty_state, render_tags
from components.navbar import render_footer
from utils.helpers import record_page_view
from utils.file_manager import file_exists, get_full_path


def render():
    record_page_view("home")

    profile = fetch_one("SELECT * FROM profile WHERE id = 1") or {}

    hero_left, hero_right = st.columns([2.2, 1])
    with hero_left:
        st.markdown('<div class="hero-badge">Available for opportunities</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-title">{profile.get("name") or "Abhishek Singh"}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-sub">{profile.get("headline", "")}</div>', unsafe_allow_html=True)
        if profile.get("about"):
            st.markdown(f'<p style="max-width:600px; margin-top:12px;">{profile["about"]}</p>', unsafe_allow_html=True)

        st.write("")
        btn_cols = st.columns([1, 1, 2])
        with btn_cols[0]:
            if st.button("Explore Projects", type="primary", use_container_width=True):
                st.switch_page("pages_public/projects.py")
        with btn_cols[1]:
            if profile.get("resume_path") and file_exists(profile["resume_path"]):
                with open(get_full_path(profile["resume_path"]), "rb") as f:
                    st.download_button("Download Resume", f, file_name="Abhishek_Singh_Resume.pdf", use_container_width=True)

    with hero_right:
        if profile.get("profile_image_path") and file_exists(profile["profile_image_path"]):
            st.image(get_full_path(profile["profile_image_path"]), use_container_width=True)

    st.write("")
    st.write("")

    # Featured projects
    st.markdown('<div class="pf-section-label">Featured Work</div>', unsafe_allow_html=True)
    st.markdown('<h3>Selected Projects</h3>', unsafe_allow_html=True)

    featured = fetch_all(
        "SELECT * FROM projects WHERE is_published = 1 AND is_featured = 1 ORDER BY created_at DESC LIMIT 6"
    )
    if not featured:
        empty_state("No featured projects yet. Mark a project as Featured in the admin panel.")
    else:
        for project in featured:
            project_card(project, on_details=lambda pid: st.session_state.update(selected_project_id=pid))

    st.write("")

    # Skills strip
    skills = fetch_all("SELECT name FROM skills ORDER BY sort_order")
    if skills:
        st.markdown('<div class="pf-section-label">Core Skills</div>', unsafe_allow_html=True)
        render_tags(", ".join([s["name"] for s in skills]))
        st.write("")

    # Experience preview
    experience = fetch_all("SELECT * FROM experience ORDER BY sort_order LIMIT 2")
    if experience:
        st.markdown('<div class="pf-section-label">Experience</div>', unsafe_allow_html=True)
        for exp in experience:
            st.markdown(f"**{exp['position']}** · {exp['company']}  \n<span style='color:#9aa1b5;font-size:0.85rem'>{exp.get('start_date','')} — {'Present' if exp.get('is_current') else exp.get('end_date','')}</span>", unsafe_allow_html=True)
        st.write("")

    # Contact strip
    st.markdown('<div class="pf-section-label">Get in Touch</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if profile.get("github_url"):
            st.link_button("GitHub", profile["github_url"], use_container_width=True)
    with c2:
        if profile.get("linkedin_url"):
            st.link_button("LinkedIn", profile["linkedin_url"], use_container_width=True)
    with c3:
        if profile.get("email"):
            st.link_button("Email", f'mailto:{profile["email"]}', use_container_width=True)

    render_footer()

render()
