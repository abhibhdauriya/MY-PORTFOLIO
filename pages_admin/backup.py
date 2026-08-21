import streamlit as st
import os
from auth.authentication import require_login
from database.backup import get_db_file_bytes, backup_filename, export_all_json, export_table_csv, EXPORT_TABLES
from database.db import DB_PATH


def render():
    require_login()
    st.markdown('<div class="hero-title" style="font-size:1.8rem;">Database Backup</div>', unsafe_allow_html=True)

    st.warning(
        "⚠️ If deployed on Streamlit Cloud, local storage is ephemeral — the app's disk (including "
        "this SQLite file and uploaded files) can be wiped on redeploy or restart. Download a backup "
        "regularly, and re-upload it after any redeploy using the restore option below."
    )

    st.markdown("### Download Full Database Backup")
    if os.path.exists(DB_PATH):
        st.download_button(
            "⬇ Download portfolio.db",
            get_db_file_bytes(),
            file_name=backup_filename(),
            mime="application/octet-stream",
            type="primary",
        )
    else:
        st.info("Database file not found yet — it will be created on first run.")

    st.markdown("### Restore from Backup")
    restore_file = st.file_uploader("Upload a previously downloaded .db file to restore", type=["db"])
    if restore_file and st.button("Restore Database (overwrites current data)"):
        with open(DB_PATH, "wb") as f:
            f.write(restore_file.getvalue())
        st.success("Database restored. Reload the app.")

    st.markdown("---")
    st.markdown("### Export Portfolio Data")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button("⬇ Export All (JSON)", export_all_json(), file_name="portfolio_export.json", mime="application/json")
    with col2:
        table = st.selectbox("Table to export as CSV", EXPORT_TABLES)
        st.download_button(f"⬇ Export {table} (CSV)", export_table_csv(table), file_name=f"{table}.csv", mime="text/csv")

render()
