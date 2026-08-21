import streamlit as st
from auth.authentication import require_login
from database.db import fetch_all, update_row, delete_row


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Contact Messages</div>', unsafe_allow_html=True)

    messages = fetch_all("SELECT * FROM contact_messages ORDER BY created_at DESC")
    if not messages:
        st.caption("No messages yet.")
        return

    for msg in messages:
        label = f"{'🔵 ' if not msg['is_read'] else ''}{msg['name']} — {msg.get('subject') or '(no subject)'} ({msg['created_at']})"
        with st.expander(label):
            st.write(f"**From:** {msg['name']} <{msg['email']}>")
            st.write(msg["message"])
            col1, col2 = st.columns(2)
            with col1:
                if not msg["is_read"] and st.button("Mark as Read", key=f"read_{msg['id']}"):
                    update_row("contact_messages", msg["id"], {"is_read": 1})
                    st.rerun()
            with col2:
                if st.button("Delete", key=f"del_msg_{msg['id']}"):
                    delete_row("contact_messages", msg["id"])
                    st.rerun()

render()
