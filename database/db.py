"""
Abhishek Singh — Portfolio CMS
Entry point. Sets up the DB, injects styles, and wires navigation.

Run locally:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Abhishek Singh | Portfolio",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.write("✅ Checkpoint 1: page_config done")

from database.db import init_db, fetch_one
st.write("✅ Checkpoint 2: db module imported")

init_db()
st.write("✅ Checkpoint 3: init_db done")

from utils.file_manager import ensure_upload_dirs
ensure_upload_dirs()
st.write("✅ Checkpoint 4: upload dirs ready")

from auth.authentication import bootstrap_admin_from_secrets, is_logged_in
bootstrap_admin_from_secrets()
st.write("✅ Checkpoint 5: admin bootstrap done")

from components.styles import inject_custom_css, inject_seo_meta
inject_custom_css()
st.write("✅ Checkpoint 6: CSS injected")

_settings = fetch_one("SELECT site_title, seo_description FROM site_settings WHERE id = 1") or {}
st.write("✅ Checkpoint 7: settings fetched")

inject_seo_meta(
    description=_settings.get("seo_description") or "MIS, Excel Automation, Python & Data Analytics portfolio.",
    site_title=_settings.get("site_title") or "Abhishek Singh | Portfolio",
)
st.write("✅ Checkpoint 8: SEO meta injected")

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
st.write("✅ Checkpoint 9: public pages list built")

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

st.write("✅ Checkpoint 10: nav structure built, about to call st.navigation")

pg = st.navigation(nav_structure)
st.write("✅ Checkpoint 11: navigation object created, about to run page")

try:
    pg.run()
    st.write("✅ Checkpoint 12: page ran successfully")
except Exception as e:
    st.error(f"Something went wrong: {e}")
    raise
