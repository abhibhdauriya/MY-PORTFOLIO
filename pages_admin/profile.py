import streamlit as st
from auth.authentication import require_login
from database.db import fetch_one, update_row
from utils.file_manager import save_uploaded_file
from utils.validators import is_valid_url, is_valid_email


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Profile</div>', unsafe_allow_html=True)

    profile = fetch_one("SELECT * FROM profile WHERE id = 1") or {}

    with st.form("profile_form"):
        name = st.text_input("Name", value=profile.get("name", ""))
        headline = st.text_input("Professional Headline", value=profile.get("headline", ""))
        about = st.text_area("About Paragraph", value=profile.get("about", ""), height=140)
        location = st.text_input("Location", value=profile.get("location", ""))
        email = st.text_input("Email", value=profile.get("email", ""))

        col1, col2 = st.columns(2)
        with col1:
            github_url = st.text_input("GitHub URL", value=profile.get("github_url", ""))
            portfolio_url = st.text_input("Portfolio URL", value=profile.get("portfolio_url", ""))
        with col2:
            linkedin_url = st.text_input("LinkedIn URL", value=profile.get("linkedin_url", ""))

        profile_image = st.file_uploader("Profile Image", type=["png", "jpg", "jpeg", "webp"])
        resume_pdf = st.file_uploader("Resume (PDF)", type=["pdf"])

        submitted = st.form_submit_button("Save Profile", type="primary")

        if submitted:
            errors = []
            if email and not is_valid_email(email):
                errors.append("Email looks invalid.")
            for url_val, label in [(github_url, "GitHub"), (linkedin_url, "LinkedIn"), (portfolio_url, "Portfolio")]:
                if url_val and not is_valid_url(url_val):
                    errors.append(f"{label} URL looks invalid.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                data = {
                    "name": name, "headline": headline, "about": about,
                    "location": location, "email": email,
                    "github_url": github_url, "linkedin_url": linkedin_url,
                    "portfolio_url": portfolio_url,
                }
                if profile_image:
                    path = save_uploaded_file(profile_image, "profile")
                    if path:
                        data["profile_image_path"] = path
                if resume_pdf:
                    path = save_uploaded_file(resume_pdf, "resume")
                    if path:
                        data["resume_path"] = path

                update_row("profile", 1, data)
                st.success("Profile updated.")
                st.rerun()

render()
