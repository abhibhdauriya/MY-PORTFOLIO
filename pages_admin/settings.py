import streamlit as st
from auth.authentication import require_login, change_password
from database.db import fetch_one, update_row


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Site Settings</div>', unsafe_allow_html=True)

    settings = fetch_one("SELECT * FROM site_settings WHERE id = 1") or {}

    with st.form("settings_form"):
        site_title = st.text_input("Website Title", value=settings.get("site_title", ""))
        subtitle = st.text_input("Subtitle", value=settings.get("subtitle", ""))
        seo_description = st.text_area("SEO Description", value=settings.get("seo_description", ""))
        footer_text = st.text_input("Footer Text", value=settings.get("footer_text", ""))
        contact_email = st.text_input("Contact Email", value=settings.get("contact_email", ""))

        submitted = st.form_submit_button("Save Settings", type="primary")
        if submitted:
            update_row("site_settings", 1, {
                "site_title": site_title, "subtitle": subtitle,
                "seo_description": seo_description, "footer_text": footer_text,
                "contact_email": contact_email,
            })
            st.success("Settings updated.")
            st.rerun()

    st.markdown("---")
    st.markdown("### Change Admin Password")
    with st.form("password_form"):
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        pw_submitted = st.form_submit_button("Update Password")
        if pw_submitted:
            if len(new_password) < 8:
                st.error("Password must be at least 8 characters.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                change_password(st.session_state.get("admin_username"), new_password)
                st.success("Password updated.")

render()
