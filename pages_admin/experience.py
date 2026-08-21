import streamlit as st
from auth.authentication import require_login
from database.db import fetch_all, insert_row, update_row, delete_row
from utils.validators import required_field_ok


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Experience</div>', unsafe_allow_html=True)

    with st.form("add_experience_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.text_input("Company *")
            start_date = st.text_input("Start Date (YYYY-MM-DD)")
            responsibilities = st.text_area("Responsibilities")
        with col2:
            position = st.text_input("Position *")
            end_date = st.text_input("End Date (YYYY-MM-DD)")
            achievements = st.text_area("Achievements")

        location = st.text_input("Location")
        is_current = st.checkbox("Current Position")
        description = st.text_area("Description")
        technologies = st.text_input("Technologies (comma separated)")

        submitted = st.form_submit_button("Add Experience", type="primary")
        if submitted:
            if not (required_field_ok(company) and required_field_ok(position)):
                st.error("Company and Position are required.")
            else:
                insert_row("experience", {
                    "company": company.strip(), "position": position.strip(),
                    "location": location, "start_date": start_date,
                    "end_date": "" if is_current else end_date,
                    "is_current": int(is_current), "description": description,
                    "responsibilities": responsibilities, "achievements": achievements,
                    "technologies": technologies,
                })
                st.success("Experience added.")
                st.rerun()

    st.markdown("---")
    entries = fetch_all("SELECT * FROM experience ORDER BY sort_order, start_date DESC")
    for exp in entries:
        with st.expander(f"{exp['position']} · {exp['company']}"):
            st.write(exp.get("description", ""))
            if st.button("Delete", key=f"del_exp_{exp['id']}"):
                delete_row("experience", exp["id"])
                st.rerun()

render()
