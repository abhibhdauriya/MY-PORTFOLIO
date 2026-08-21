import streamlit as st
from auth.authentication import require_login
from database.db import fetch_all, insert_row, delete_row
from utils.file_manager import save_uploaded_file, delete_file
from utils.validators import required_field_ok, is_valid_url


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Certificates</div>', unsafe_allow_html=True)

    with st.form("add_cert_form"):
        title = st.text_input("Title *")
        col1, col2 = st.columns(2)
        with col1:
            issuing_org = st.text_input("Issuing Organization")
            credential_url = st.text_input("Credential URL")
        with col2:
            issue_date = st.text_input("Date (YYYY-MM-DD)")
        description = st.text_area("Description")
        cert_file = st.file_uploader("Certificate File (image or PDF)", type=["png", "jpg", "jpeg", "webp", "pdf"])

        submitted = st.form_submit_button("Add Certificate", type="primary")
        if submitted:
            errors = []
            if not required_field_ok(title):
                errors.append("Title is required.")
            if credential_url and not is_valid_url(credential_url):
                errors.append("Credential URL looks invalid.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                data = {
                    "title": title.strip(), "issuing_org": issuing_org,
                    "issue_date": issue_date, "credential_url": credential_url,
                    "description": description,
                }
                if cert_file:
                    path = save_uploaded_file(cert_file, "certificates")
                    if path:
                        data["file_path"] = path
                insert_row("certificates", data)
                st.success("Certificate added.")
                st.rerun()

    st.markdown("---")
    certs = fetch_all("SELECT * FROM certificates ORDER BY issue_date DESC")
    for cert in certs:
        cols = st.columns([4, 1])
        with cols[0]:
            st.write(f"**{cert['title']}** — {cert.get('issuing_org','')} ({cert.get('issue_date','')})")
        with cols[1]:
            if st.button("Delete", key=f"del_cert_{cert['id']}"):
                delete_file(cert.get("file_path"))
                delete_row("certificates", cert["id"])
                st.rerun()

render()
