import streamlit as st
from auth.authentication import verify_login, login, is_logged_in
from database.db import fetch_one


def render():
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Admin Login</div>', unsafe_allow_html=True)
    st.write("")

    if is_logged_in():
        st.switch_page("pages_admin/dashboard.py")
        return

    admin_exists = fetch_one("SELECT id FROM admin_users LIMIT 1")
    if not admin_exists:
        st.warning(
            "No admin account is configured yet. Add `admin_username` and `admin_password` "
            "to `.streamlit/secrets.toml` (local) or your Streamlit Cloud app secrets, then reload."
        )
        return

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In", type="primary")

        if submitted:
            if verify_login(username, password):
                login(username)
                st.rerun()
            else:
                st.error("Invalid username or password.")


render()