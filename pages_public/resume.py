import streamlit as st
from database.db import fetch_one, fetch_all
from components.navbar import render_page_title, render_footer
from components.cards import empty_state
from utils.helpers import record_page_view, csv_to_list
from utils.file_manager import file_exists, get_full_path


def render():
    record_page_view("resume")
    render_page_title("Resume", "Resume")

    profile = fetch_one("SELECT * FROM profile WHERE id = 1") or {}

    if profile.get("resume_path") and file_exists(profile["resume_path"]):
        with open(get_full_path(profile["resume_path"]), "rb") as f:
            st.download_button("⬇ Download Resume (PDF)", f, file_name="Abhishek_Singh_Resume.pdf", type="primary")
        st.write("")
    else:
        st.info("A downloadable PDF resume will appear here once uploaded in the admin panel.")

    st.markdown("---")
    st.markdown("### Summary")
    st.markdown(profile.get("about") or "_Not added yet._")

    st.markdown("### Experience")
    experience = fetch_all("SELECT * FROM experience ORDER BY sort_order, start_date DESC")
    if not experience:
        empty_state("No experience entries yet.")
    for exp in experience:
        date_range = f'{exp.get("start_date","")} — {"Present" if exp.get("is_current") else exp.get("end_date","")}'
        st.markdown(f"**{exp['position']}**, {exp['company']}  \n*{date_range}*")
        if exp.get("description"):
            st.markdown(exp["description"])
        st.write("")

    st.markdown("### Skills")
    skills = fetch_all("SELECT name FROM skills ORDER BY sort_order")
    if skills:
        st.markdown(", ".join(s["name"] for s in skills))

    st.markdown("### Projects")
    projects = fetch_all("SELECT title, short_description FROM projects WHERE is_published = 1 ORDER BY created_at DESC LIMIT 6")
    for p in projects:
        st.markdown(f"**{p['title']}** — {p['short_description']}")

    st.markdown("### Certifications")
    certs = fetch_all("SELECT title, issuing_org, issue_date FROM certificates ORDER BY issue_date DESC")
    for c in certs:
        st.markdown(f"**{c['title']}** — {c['issuing_org']} ({c['issue_date']})")

    st.markdown("### Contact")
    contact_bits = csv_to_list(", ".join(filter(None, [profile.get("email"), profile.get("github_url"), profile.get("linkedin_url")])))
    st.markdown(" · ".join(contact_bits) if contact_bits else "_Not added yet._")

    render_footer()

render()
