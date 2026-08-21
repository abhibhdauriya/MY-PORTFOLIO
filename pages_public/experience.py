import streamlit as st
from database.db import fetch_all
from components.navbar import render_page_title, render_footer
from components.cards import experience_card, empty_state
from utils.helpers import record_page_view


def render():
    record_page_view("experience")
    render_page_title("Career", "Experience")

    experience = fetch_all("SELECT * FROM experience ORDER BY sort_order, start_date DESC")
    if not experience:
        empty_state("Experience entries will appear here once added in the admin panel.")
    else:
        for exp in experience:
            experience_card(exp)

    render_footer()

render()
