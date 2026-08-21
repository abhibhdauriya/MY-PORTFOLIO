import streamlit as st
from auth.authentication import require_login
from database.db import fetch_all, insert_row, update_row, delete_row
from utils.validators import required_field_ok, is_valid_url

LINK_CATEGORIES = ["GitHub Repository", "Live Website", "Streamlit App", "Excel Demo", "Documentation", "YouTube Demo", "LinkedIn", "Other"]


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Links Manager</div>', unsafe_allow_html=True)

    with st.form("add_link_form"):
        title = st.text_input("Title *")
        url = st.text_input("URL *")
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", LINK_CATEGORIES)
        with col2:
            icon = st.text_input("Icon (emoji, optional)")
        description = st.text_area("Description")
        col3, col4 = st.columns(2)
        with col3:
            is_featured = st.checkbox("Featured")
        with col4:
            is_active = st.checkbox("Active", value=True)

        submitted = st.form_submit_button("Add Link", type="primary")
        if submitted:
            errors = []
            if not required_field_ok(title):
                errors.append("Title is required.")
            if not is_valid_url(url) or not url:
                errors.append("A valid URL is required.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                insert_row("links", {
                    "title": title.strip(), "url": url.strip(), "description": description,
                    "category": category, "icon": icon, "is_featured": int(is_featured),
                    "is_active": int(is_active),
                })
                st.success("Link added.")
                st.rerun()

    st.markdown("---")
    links = fetch_all("SELECT * FROM links ORDER BY created_at DESC")
    for link in links:
        cols = st.columns([3, 2, 1, 1])
        with cols[0]:
            st.write(f"**{link['title']}**")
            st.caption(link["url"])
        with cols[1]:
            st.caption(link["category"])
        with cols[2]:
            if st.button("Toggle Active", key=f"active_{link['id']}"):
                update_row("links", link["id"], {"is_active": 0 if link["is_active"] else 1})
                st.rerun()
        with cols[3]:
            if st.button("Delete", key=f"del_link_{link['id']}"):
                delete_row("links", link["id"])
                st.rerun()

render()
