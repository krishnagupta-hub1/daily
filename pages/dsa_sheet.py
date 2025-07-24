#divide file main daily_app.py
import streamlit as st
import threading
import time
import datetime

from core.data_handler import load_data, save_data
from core.date_utils import get_display_date, get_now_datetime

# Import all pages (from /pages folder)
from pages import (
    home,
    afternoon_schedule,
    classroom_studies,
    dsa_sheet,
    balanced_diet,
    mind_body,
    time_reminder,
    dairy,
    stored_data,
    important_dates,
    passwords,
    details_portfolio,
    app_update
)

# -------------------------
# Session State Initialization
# -------------------------
data = load_data()

DEFAULTS = {
    "classroom_tasks": {
        "Database System": [],
        "Operating Systems": [],
        "Compiler Design": [],
        "Computer Networks": [],
        "Cloud Architecture Design": [],
    },
    "completed_classroom_tasks": {
        "Database System": {},
        "Operating Systems": {},
        "Compiler Design": {},
        "Computer Networks": {},
        "Cloud Architecture Design": {},
    },
    "app_updates": [],
    "app_ideas": [],
    "duolingo_records": {},
    "morning_exercise_records": {},
    "jawline_records": {},
    "dairy_records": {},
    "water_counts": {},
    "water_checklists": {},
    "water_main_checklist": {},
    "passwords": {
        "Folder 1": [],
        "Folder 2": [],
        "Folder 3": [],
        "Folder 4": [],
    },
    "dsa_sheet": [{} for _ in range(18)],
    "important_dates": []
}

for key, default in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = data.get(key, default)

# -------------------------
# Sidebar Navigation
# -------------------------
st.sidebar.title("📘 Navigation")

PAGES = {
    "Home": home.draw,
    "Afternoon Schedule": afternoon_schedule.draw,
    "Classroom Studies": classroom_studies.draw,
    "DSA Sheet Scheduling": dsa_sheet.draw,
    "Balanced Diet": balanced_diet.draw,
    "Mind & Body Routine": mind_body.draw,
    "Time Reminder": time_reminder.draw,
    "Dairy": dairy.draw,
    "Stored Data": stored_data.draw,
    "Important Dates": important_dates.draw,
    "Passwords": passwords.draw,
    "Details and Portfolio": details_portfolio.draw,
    "App Update": app_update.draw
}

page = st.sidebar.radio("Go to", list(PAGES.keys()))

# -------------------------
# Top Header with Clock
# -------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"## 📅 Today's Date: {get_display_date()}")
with col2:
    timer_placeholder = st.empty()

def update_clock():
    while True:
        timer_placeholder.markdown(
            f"<div style='text-align:right;font-size:20px;background:#000000;color:#39FF14;padding:8px;border-radius:8px;'>🕒 Timers: {get_now_datetime().strftime('%H:%M:%S')}</div>",
            unsafe_allow_html=True
        )
        time.sleep(1)

thread = threading.Thread(target=update_clock)
thread.daemon = True
thread.start()

# -------------------------
# Render the Selected Page
# -------------------------
PAGES[page]()











