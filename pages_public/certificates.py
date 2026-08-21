import streamlit as st
from database.db import fetch_all
from components.navbar import render_page_title, render_footer
from components.cards import certificate_card, empty_state
from utils.helpers import record_page_view


def render():
    record_page_view("certificates")
    render_page_title("Credentials", "Certificates")

    certs = fetch_all("SELECT * FROM certificates ORDER BY issue_date DESC")
    if not certs:
        empty_state("Certificates will appear here once added in the admin panel.")
    else:
        cols = st.columns(2)
        for i, cert in enumerate(certs):
            with cols[i % 2]:
                certificate_card(cert)

    render_footer()

render()
