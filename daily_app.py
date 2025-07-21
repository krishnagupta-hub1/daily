import streamlit as st
import datetime
import time
import threading
import json
import os

st.set_page_config(layout="wide", page_title="Daily Tracker")

# --- Helper Functions for Persistence ---
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {"classroom_tasks": [], "app_updates": [], "app_ideas": []}

def save_data():
    with open("data.json", "w") as f:
        json.dump({
            "classroom_tasks": st.session_state.classroom_tasks,
            "app_updates": st.session_state.app_updates,
            "app_ideas": st.session_state.app_ideas
        }, f)

# --- Session Setup ---
data = load_data()

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "classroom_tasks" not in st.session_state:
    st.session_state.classroom_tasks = data["classroom_tasks"]
if "app_updates" not in st.session_state:
    st.session_state.app_updates = data["app_updates"]
if "app_ideas" not in st.session_state:
    st.session_state.app_ideas = data["app_ideas"]

# --- Sidebar Navigation ---
st.sidebar.title("📘 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Afternoon Schedule",
    "Classroom Studies",
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
    <div style='background-color:#e6ffe6;padding:15px;border-radius:10px;margin-top:10px;'>
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
    <div style='background-color:#f5f5f5;padding:20px;border-radius:10px;margin-top:25px;'>
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
    <div style='background-color:#ffe6e6;padding:20px;border-radius:10px;margin-top:25px;'>
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
    <div style='background-color:#e6ffe6;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>📘 DUOLINGO</h4>
    </div>
    """, unsafe_allow_html=True)
    st.checkbox("100 - 150 XP completed", key="duolingo_afternoon")

elif page == "Classroom Studies":
    st.title("📚 Classroom Studies")
    task = st.text_input("Enter your study topic for today:")
    date = st.date_input("Select the date for this task")

    if st.button("Submit Study Task"):
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
    st.write("Access all your saved entries and reminders here.")

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
