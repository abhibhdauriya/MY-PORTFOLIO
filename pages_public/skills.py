import streamlit as st
from database.db import fetch_all
from components.navbar import render_page_title, render_footer
from components.cards import empty_state
from utils.helpers import SKILL_CATEGORIES, record_page_view


def render():
    record_page_view("skills")
    render_page_title("Skills", "Technical Skills")

    all_skills = fetch_all("SELECT * FROM skills ORDER BY category, sort_order")
    if not all_skills:
        empty_state("Skills will appear here once added in the admin panel.")
        render_footer()
        return

    for category in SKILL_CATEGORIES:
        items = [s for s in all_skills if s["category"] == category]
        if not items:
            continue
        st.markdown(f"### {category}")
        cols = st.columns(4)
        for i, skill in enumerate(items):
            with cols[i % 4]:
                level_str = f" · {skill['level']}" if skill.get("level") else ""
                st.markdown(
                    f'<div class="pf-card" style="text-align:center; padding:14px;">'
                    f'<b>{skill["name"]}</b><br><span style="font-size:0.78rem;color:#9aa1b5;">{level_str}</span></div>',
                    unsafe_allow_html=True,
                )
        st.write("")

    render_footer()

render()
