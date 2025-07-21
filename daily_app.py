import streamlit as st
import datetime
import time
import threading
import json
import os
import calendar

st.set_page_config(layout="wide", page_title="Daily Tracker")

# --- Helper Functions for Persistence ---
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    # Add new duolingo_records to store checklist per date
    return {
        "classroom_tasks": [],
        "app_updates": [],
        "app_ideas": [],
        "duolingo_records": {}  # {"2025-07-21": true, ...}
    }

def save_data():
    with open("data.json", "w") as f:
        json.dump({
            "classroom_tasks": st.session_state.classroom_tasks,
            "app_updates": st.session_state.app_updates,
            "app_ideas": st.session_state.app_ideas,
            "duolingo_records": st.session_state.duolingo_records
        }, f)

# --- Session Setup ---
data = load_data()

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "classroom_tasks" not in st.session_state:
    st.session_state.classroom_tasks = data.get("classroom_tasks", [])
if "app_updates" not in st.session_state:
    st.session_state.app_updates = data.get("app_updates", [])
if "app_ideas" not in st.session_state:
    st.session_state.app_ideas = data.get("app_ideas", [])
if "duolingo_records" not in st.session_state:
    st.session_state.duolingo_records = data.get("duolingo_records", {})

# --- Sidebar Navigation ---
st.sidebar.title("📘 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Afternoon Schedule",
    "DSA Sheet Scheduling",
    "Balanced Diet",
    "Mind & Body Routine",
    "Time Reminder",
    "Details and Portfolio",
    "Stored Data",
    "App Update"
])
st.session_state.page = page

# --- Top Header ---
col1, col2 = st.columns([3, 1])
with col1:
    today = datetime.date.today()
    st.markdown(f"## 📅 Today's Date: {today.strftime('%A, %d %B %Y')}")
with col2:
    timer_placeholder = st.empty()

# --- Digital Clock ---
def update_clock():
    while True:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        timer_placeholder.markdown(
            f"<div style='text-align:right;font-size:20px;background:#000000;color:#39FF14;padding:8px;border-radius:8px;'>🕒 Timers: {now}</div>",
            unsafe_allow_html=True
        )
        time.sleep(1)

thread = threading.Thread(target=update_clock)
thread.daemon = True
thread.start()

# --- Pages ---
if page == "Home":
    st.title("🏠 Welcome to Your Daily App")
    for i in range(1, 7):
        st.markdown(f"<div style='background-color:#d0ebff;padding:15px;border-radius:10px;margin-top:10px;'>🔹 Section {i}</div>", unsafe_allow_html=True)

    st.markdown("""<hr style='margin-top:30px;margin-bottom:10px;border:1px solid #ccc;'>""", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:16px;color:#888;'>
        <strong>#At Night</strong><br>
        Update dairy / Twitter / Git<br>
        Check mails / LinkedIn / Organisation / Instagram<br>
        (search / commitChanges)<br>
        - &nbsp;&nbsp;&nbsp; - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color:#e6ffe6;color:#000000;padding:15px;border-radius:10px;margin-top:10px;'>
        <h4>📘 DUOLINGO</h4>
        <label>
            <input type='checkbox' style='margin-right:10px;'>100 - 150 XP completed
        </label>
    </div>
    """, unsafe_allow_html=True)

elif page == "Afternoon Schedule":
    st.title("🕑 Afternoon Schedule")
    st.write("Add your afternoon tasks or routines here.")

    # Morning Exercise - Light Grey
    st.markdown("""
    <div style='background-color:#f5f5f5;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>🏃‍♂️ Morning 30 min Exercise</h4>
        <ul>
            <li>Pushups 30</li>
            <li>Crunches 30</li>
            <li>Side planks or Russian twist 30</li>
            <li>Bhujangasana 30 sec</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Jawline Routine - Light Red
    st.markdown("""
    <div style='background-color:#ffe6e6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>😁 Jawline Routine</h4>
        <h5>1. Warm Up</h5>
        <ul>
            <li>Upward stretch</li>
            <li>Face upward rotate 180</li>
            <li>Stretching face both sides</li>
        </ul>
        <h5>2. Vid 1</h5>
        <p>**[Video Placeholder for Vid 1]**</p>
        <h5>3. Vid 2</h5>
        <p>**[Video Placeholder for Vid 2]**</p>
    </div>
    """, unsafe_allow_html=True)

    # Duolingo - Light Green
    st.markdown("""
    <div style='background-color:#e6ffe6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>📘 DUOLINGO</h4>
    </div>
    """, unsafe_allow_html=True)

    # Track Duolingo checklist for today in calendar
    today_str = datetime.date.today().isoformat()
    duolingo_done = st.checkbox("100 - 150 XP completed", key=f"duolingo_afternoon_{today_str}")

    # Save state if checked/unchecked
    prev_val = st.session_state.duolingo_records.get(today_str, None)
    # If it's newly changed, or not present, save
    if duolingo_done != prev_val:
        st.session_state.duolingo_records[today_str] = duolingo_done
        save_data()

    st.markdown("""<hr style='margin-top:35px;margin-bottom:10px;border:1px solid #ccc;'>""", unsafe_allow_html=True)
    # --- New Classroom Studies Section ---
    st.markdown("""<div style='background-color:#d0ebff;padding:18px 15px 12px 15px;border-radius:10px;margin-top:10px;'>
        <h4>📚 Classroom Studies</h4>
        <div style='color:#333;font-size:15px;margin-bottom:8px;'>
            Track your daily study topics and dates.
        </div>
    </div>""", unsafe_allow_html=True)

    with st.form(key="classroom_studies_form"):
        task = st.text_input("Enter your study topic for today:")
        date = st.date_input("Select the date for this task")
        submitted = st.form_submit_button("Submit Study Task")
        if submitted:
            if task:
                st.session_state.classroom_tasks.append((task, str(date)))
                save_data()
            else:
                st.warning("Please enter a task before submitting.")

    for t, d in st.session_state.classroom_tasks:
        st.markdown(
            f"<div style='background:#d0ebff;padding:10px;margin-top:5px;border-radius:8px;'>📝 {t} <span style='float:right;'>📅 {d}</span></div>",
            unsafe_allow_html=True
        )

elif page == "DSA Sheet Scheduling":
    st.title("🧠 DSA Sheet Scheduling")
    st.write("Plan your DSA problems here.")

elif page == "Balanced Diet":
    st.title("🥗 Balanced Diet")
    st.write("Log your meals and nutrition here.")

elif page == "Mind & Body Routine":
    st.title("🧘 Mind & Body Routine")
    st.write("Track your fitness or wellness exercises.")

elif page == "Time Reminder":
    st.title("⏰ Time Reminder")
    st.write("Set and manage time-based reminders.")

elif page == "Details and Portfolio":
    st.title("📁 Details and Portfolio")
    st.markdown("### Connect with Me")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/instagram-new.png", width=80)
        if st.button("Instagram"):
            st.markdown("[Click here](https://www.instagram.com/krishnagupta___07/?__pwa=1)", unsafe_allow_html=True)

    with col2:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/github.png", width=80)
        if st.button("GitHub"):
            st.markdown("[Click here](https://github.com/krishnagupta-hub1)", unsafe_allow_html=True)

    with col3:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/linkedin.png", width=80)
        if st.button("LinkedIn"):
            st.markdown("[Click here](https://www.linkedin.com/in/krishna-gupta-63b354216)", unsafe_allow_html=True)

    with col4:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/twitterx.png", width=80)
        if st.button("Twitter (X)"):
            st.markdown("[Click here](https://x.com/KrishnaGup72761)", unsafe_allow_html=True)

elif page == "Stored Data":
    st.title("🗃️ Stored Data")
    st.markdown("#### Six divisions are shown below. First division: Your Duolingo Checklist Calendar")

    # -- Division 1: Duolingo Checklist Calendar --
    st.markdown("##### Division 1: <span style='color:#39FF14'>Duolingo Activity Calendar</span>", unsafe_allow_html=True)

    # Calendar for current month
    today = datetime.date.today()
    year = today.year
    month = today.month

    duolingo_records = st.session_state.duolingo_records

    month_cal = calendar.monthcalendar(year, month)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Prepare for colored icons: green tick, red cross
    tick = "<span style='color:green;font-size:22px;'>&#10003;</span>"
    cross = "<span style='color:red;font-size:22px;'>&#10007;</span>"

    # Render the calendar table with tick/cross for each day
    table_html = f"<table style='width:100%;text-align:center;font-size:16px;'><tr>"
    for d in days:
        table_html += f"<th style='padding:2px 8px 2px 8px;'>{d}</th>"
    table_html += "</tr>"

    for week in month_cal:
        table_html += "<tr>"
        for day in week:
            if day == 0:
                table_html += "<td></td>"
            else:
                day_str = datetime.date(year, month, day).isoformat()
                mark = tick if duolingo_records.get(day_str, False) else cross
                table_html += f"<td style='padding:7px'>{day}<br>{mark}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.info("A green tick means Duolingo checklist was marked as completed for that day. A red cross means it was not done.")

    # -- Division 2 to 6: Placeholders --
    for idx in range(2, 7):
        st.markdown(f"""<div style='background-color:#ffe6e6;padding:15px;border-radius:10px;margin-top:15px;margin-bottom:10px;'>
            <strong>Division {idx}:</strong> <span style='color:#888;'>[Your custom data or tracker here]</span>
        </div>""", unsafe_allow_html=True)

elif page == "App Update":
    st.title("🔄 App Update")

    left_col, right_col = st.columns(2)

    with left_col:
        todays_update = st.text_input("", placeholder="Today's Update")
        if st.button("Submit Update") and todays_update:
            st.session_state.app_updates.append(todays_update)
            save_data()
        if st.button("Delete Last Update") and st.session_state.app_updates:
            st.session_state.app_updates.pop()
            save_data()
        for i, upd in enumerate(st.session_state.app_updates, 1):
            st.markdown(f"**{i}.** {upd}")

    with right_col:
        another_idea = st.text_input(" ", placeholder="Another Idea")
        if st.button("Submit Idea") and another_idea:
            st.session_state.app_ideas.append(another_idea)
            save_data()
        if st.button("Delete Last Idea") and st.session_state.app_ideas:
            st.session_state.app_ideas.pop()
            save_data()
        for i, idea in enumerate(st.session_state.app_ideas, 1):
            st.markdown(f"**{i}.** {idea}")

