import streamlit as st
from auth.authentication import require_login, logout
from database.db import fetch_all, fetch_one


def render():
    require_login()

    top = st.columns([4, 1])
    with top[0]:
        st.markdown('<div class="hero-title" style="font-size:1.8rem;">Admin Dashboard</div>', unsafe_allow_html=True)
    with top[1]:
        if st.button("Logout", use_container_width=True):
            logout()
            st.switch_page("pages_public/home.py")

    st.write("")

    counts = {
        "Total Projects": fetch_one("SELECT COUNT(*) c FROM projects")["c"],
        "Excel/VBA Projects": fetch_one("SELECT COUNT(*) c FROM projects WHERE category IN ('Excel Automation','VBA')")["c"],
        "Web Projects": fetch_one("SELECT COUNT(*) c FROM projects WHERE category = 'Web Development'")["c"],
        "Certificates": fetch_one("SELECT COUNT(*) c FROM certificates")["c"],
        "Skills": fetch_one("SELECT COUNT(*) c FROM skills")["c"],
        "Page Views": fetch_one("SELECT COUNT(*) c FROM page_views")["c"],
    }

    cols = st.columns(3)
    for i, (label, value) in enumerate(counts.items()):
        with cols[i % 3]:
            st.markdown(
                f'<div class="pf-card" style="text-align:center;">'
                f'<div style="font-size:1.8rem;font-weight:800;color:#f1f3f8;">{value}</div>'
                f'<div style="font-size:0.8rem;color:#9aa1b5;">{label}</div></div>',
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown("### Recently Added Projects")
    recent = fetch_all("SELECT title, category, created_at FROM projects ORDER BY created_at DESC LIMIT 5")
    if recent:
        for r in recent:
            st.markdown(f"- **{r['title']}** ({r['category']}) — {r['created_at']}")
    else:
        st.caption("No projects yet.")

    st.write("")
    st.markdown("### Recently Updated Projects")
    updated = fetch_all("SELECT title, category, updated_at FROM projects ORDER BY updated_at DESC LIMIT 5")
    if updated:
        for r in updated:
            st.markdown(f"- **{r['title']}** ({r['category']}) — {r['updated_at']}")
    else:
        st.caption("No projects yet.")

    unread = fetch_one("SELECT COUNT(*) c FROM contact_messages WHERE is_read = 0")["c"]
    if unread:
        st.info(f"You have {unread} unread contact message(s).")

render()
