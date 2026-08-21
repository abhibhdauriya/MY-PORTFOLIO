"""
Admin authentication: bcrypt password hashing, session-state login gate,
and first-run bootstrap of the admin account from st.secrets.
"""

import bcrypt
import streamlit as st
from database.db import fetch_one, insert_row, get_conn


def bootstrap_admin_from_secrets():
    """
    On first run, if no admin_users row exists, create one from
    st.secrets["admin_username"] / st.secrets["admin_password"].
    This lets you set credentials via .streamlit/secrets.toml (local)
    or the Streamlit Cloud secrets manager (deployed) without ever
    hardcoding a password in source.
    """
    existing = fetch_one("SELECT id FROM admin_users LIMIT 1")
    if existing:
        return

    try:
        username = st.secrets["admin_username"]
        password = st.secrets["admin_password"]
    except (KeyError, FileNotFoundError):
        # No secrets configured yet — admin panel will show a setup message.
        return

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    insert_row("admin_users", {"username": username, "password_hash": password_hash})


def verify_login(username: str, password: str) -> bool:
    user = fetch_one("SELECT * FROM admin_users WHERE username = ?", (username,))
    if not user:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8"))


def is_logged_in() -> bool:
    return st.session_state.get("is_admin_logged_in", False)


def login(username: str):
    st.session_state["is_admin_logged_in"] = True
    st.session_state["admin_username"] = username


def logout():
    st.session_state["is_admin_logged_in"] = False
    st.session_state.pop("admin_username", None)


def change_password(username: str, new_password: str):
    password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    with get_conn() as conn:
        conn.execute(
            "UPDATE admin_users SET password_hash = ? WHERE username = ?",
            (password_hash, username),
        )


def require_login():
    """Call at the top of every admin page. Redirects to login if not authenticated."""
    if not is_logged_in():
        st.warning("Please log in to access the admin panel.")
        st.stop()
