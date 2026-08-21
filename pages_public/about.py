import streamlit as st
from database.db import fetch_one
from components.navbar import render_page_title, render_footer
from utils.helpers import record_page_view
from utils.file_manager import file_exists, get_full_path


def render():
    record_page_view("about")
    profile = fetch_one("SELECT * FROM profile WHERE id = 1") or {}

    render_page_title("About", "About Me")

    col1, col2 = st.columns([1, 2.2])
    with col1:
        if profile.get("profile_image_path") and file_exists(profile["profile_image_path"]):
            st.image(get_full_path(profile["profile_image_path"]), use_container_width=True)
        if profile.get("location"):
            st.markdown(f"📍 {profile['location']}")
        if profile.get("email"):
            st.markdown(f"✉️ {profile['email']}")

    with col2:
        st.markdown(f'<h3>{profile.get("headline","")}</h3>', unsafe_allow_html=True)
        st.markdown(profile.get("about") or "*Profile content coming soon — set it up in the admin panel.*")

    render_footer()

render()
