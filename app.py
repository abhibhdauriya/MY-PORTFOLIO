"""
Abhishek Singh — Portfolio CMS
Entry point. Sets up the DB, injects styles, and wires navigation.

Run locally:  streamlit run app.py
"""

import streamlit as st
from database.db import init_db, fetch_one
from auth.authentication import bootstrap_admin_from_secrets, is_logged_in
from components.styles import inject_custom_css, inject_seo_meta
from utils.file_manager import ensure_upload_dirs

st.set_page_config(
    page_title="Abhishek Singh | Portfolio",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded",
)

# --- One-time setup ---
init_db()
ensure_upload_dirs()
bootstrap_admin_from_secrets()
inject_custom_css()

_settings = fetch_one("SELECT site_title, seo_description FROM site_settings WHERE id = 1") or {}
inject_seo_meta(
    description=_settings.get("seo_description") or "MIS, Excel Automation, Python & Data Analytics portfolio.",
    site_title=_settings.get("site_title") or "Abhishek Singh | Portfolio",
)

# --- Navigation: file-based pages, so st.switch_page("pages_public/x.py") works ---
public_pages = [
    st.Page("pages_public/home.py", title="Home", icon="🏠", url_path="home", default=True),
    st.Page("pages_public/about.py", title="About Me", icon="👤", url_path="about"),
    st.Page("pages_public/skills.py", title="Skills", icon="🛠️", url_path="skills"),
    st.Page("pages_public/experience.py", title="Experience", icon="💼", url_path="experience"),
    st.Page("pages_public/projects.py", title="Projects", icon="📁", url_path="projects"),
    st.Page("pages_public/excel.py", title="Excel & VBA Automation", icon="📊", url_path="excel"),
    st.Page("pages_public/web_apps.py", title="Web Applications", icon="🌐", url_path="web-apps"),
    st.Page("pages_public/resume.py", title="Resume", icon="📄", url_path="resume"),
    st.Page("pages_public/certificates.py", title="Certificates", icon="🎓", url_path="certificates"),
    st.Page("pages_public/contact.py", title="Contact", icon="✉️", url_path="contact"),
]

if is_logged_in():
    admin_nav_pages = [
        st.Page("pages_admin/dashboard.py", title="Dashboard", icon="📈", url_path="admin-dashboard"),
        st.Page("pages_admin/profile.py", title="Profile", icon="👤", url_path="admin-profile"),
        st.Page("pages_admin/projects.py", title="Projects", icon="📁", url_path="admin-projects"),
        st.Page("pages_admin/skills.py", title="Skills", icon="🛠️", url_path="admin-skills"),
        st.Page("pages_admin/experience.py", title="Experience", icon="💼", url_path="admin-experience"),
        st.Page("pages_admin/certificates.py", title="Certificates", icon="🎓", url_path="admin-certificates"),
        st.Page("pages_admin/links.py", title="Links", icon="🔗", url_path="admin-links"),
        st.Page("pages_admin/messages.py", title="Messages", icon="📬", url_path="admin-messages"),
        st.Page("pages_admin/settings.py", title="Site Settings", icon="⚙️", url_path="admin-settings"),
        st.Page("pages_admin/backup.py", title="Database Backup", icon="💾", url_path="admin-backup"),
    ]
    nav_structure = {"Portfolio": public_pages, "Admin": admin_nav_pages}
else:
    admin_auth_pages = [
        st.Page("pages_public/admin_login.py", title="Admin Login", icon="🔐", url_path="admin-login"),
    ]
    nav_structure = {"Portfolio": public_pages, "Admin": admin_auth_pages}

pg = st.navigation(nav_structure)

try:
    pg.run()
except Exception as e:
    if is_logged_in():
        # Admin sees the real error for debugging
        st.error(f"Something went wrong: {e}")
        raise
    else:
        st.error("Something went wrong while loading this page. Please try again shortly.")

