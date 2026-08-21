import streamlit as st
from database.db import fetch_one, insert_row
from components.navbar import render_page_title, render_footer
from utils.validators import is_valid_email, required_field_ok
from utils.helpers import record_page_view


def render():
    record_page_view("contact")
    render_page_title("Contact", "Get in Touch", "Have a project, role, or question in mind? Send a message below.")

    profile = fetch_one("SELECT * FROM profile WHERE id = 1") or {}

    col1, col2 = st.columns([1.5, 1])

    with col1:
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Name *")
            email = st.text_input("Email *")
            subject = st.text_input("Subject")
            message = st.text_area("Message *", height=140)
            submitted = st.form_submit_button("Send Message", type="primary")

            if submitted:
                errors = []
                if not required_field_ok(name):
                    errors.append("Name is required.")
                if not is_valid_email(email):
                    errors.append("A valid email is required.")
                if not required_field_ok(message):
                    errors.append("Message cannot be empty.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    insert_row("contact_messages", {
                        "name": name.strip(), "email": email.strip(),
                        "subject": subject.strip(), "message": message.strip(),
                    })
                    st.success("Message sent — thanks for reaching out! I'll get back to you soon.")

    with col2:
        st.markdown("#### Connect")
        if profile.get("email"):
            st.markdown(f"✉️ [{profile['email']}](mailto:{profile['email']})")
        if profile.get("github_url"):
            st.markdown(f"💻 [GitHub]({profile['github_url']})")
        if profile.get("linkedin_url"):
            st.markdown(f"🔗 [LinkedIn]({profile['linkedin_url']})")
        if profile.get("location"):
            st.markdown(f"📍 {profile['location']}")

    render_footer()

render()
