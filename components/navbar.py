"""
Navbar (hero identity block used on public pages) and footer.
Actual navigation is handled by st.navigation in app.py — this renders
the visual header content within each page.
"""

import streamlit as st
from database.db import fetch_one


def render_footer():
    settings = fetch_one("SELECT footer_text FROM site_settings WHERE id = 1") or {}
    footer_text = settings.get("footer_text") or "© Abhishek Singh. Built with Python + Streamlit."
    st.markdown("---")
    st.markdown(
        f'<div style="text-align:center; color:#6b7280; font-size:0.85rem; padding:10px 0;">{footer_text}</div>',
        unsafe_allow_html=True,
    )


def render_page_title(label: str, title: str, subtitle: str = ""):
    st.markdown(f'<div class="pf-section-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title" style="font-size:2rem;">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="hero-sub">{subtitle}</div>', unsafe_allow_html=True)
    st.write("")
