import streamlit as st
from auth.authentication import require_login
from database.db import fetch_all, insert_row, update_row, delete_row
from utils.helpers import SKILL_CATEGORIES
from utils.validators import required_field_ok


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Skills</div>', unsafe_allow_html=True)

    with st.form("add_skill_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Skill Name *")
        with col2:
            category = st.selectbox("Category", SKILL_CATEGORIES)
        with col3:
            level = st.text_input("Level (optional)", placeholder="e.g. Advanced")
        submitted = st.form_submit_button("Add Skill", type="primary")
        if submitted:
            if not required_field_ok(name):
                st.error("Skill name is required.")
            else:
                insert_row("skills", {"name": name.strip(), "category": category, "level": level.strip()})
                st.success("Skill added.")
                st.rerun()

    st.markdown("---")
    skills = fetch_all("SELECT * FROM skills ORDER BY category, sort_order")
    for skill in skills:
        cols = st.columns([2, 2, 2, 1])
        with cols[0]:
            st.write(skill["name"])
        with cols[1]:
            st.caption(skill["category"])
        with cols[2]:
            st.caption(skill.get("level") or "—")
        with cols[3]:
            if st.button("Delete", key=f"del_skill_{skill['id']}"):
                delete_row("skills", skill["id"])
                st.rerun()

render()
