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
    return {
        "classroom_tasks": [],
        "app_updates": [],
        "app_ideas": [],
        "duolingo_records": {},
        "morning_exercise_records": {},
        "jawline_records": {},
        "dairy_records": {},            # Add dairy entries by day
        "last_reset_date": ""
    }

def save_data():
    with open("data.json", "w") as f:
        json.dump({
            "classroom_tasks": st.session_state.classroom_tasks,
            "app_updates": st.session_state.app_updates,
            "app_ideas": st.session_state.app_ideas,
            "duolingo_records": st.session_state.duolingo_records,
            "morning_exercise_records": st.session_state.morning_exercise_records,
            "jawline_records": st.session_state.jawline_records,
            "dairy_records": st.session_state.dairy_records,
            "last_reset_date": st.session_state.last_reset_date
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
if "morning_exercise_records" not in st.session_state:
    st.session_state.morning_exercise_records = data.get("morning_exercise_records", {})
if "jawline_records" not in st.session_state:
    st.session_state.jawline_records = data.get("jawline_records", {})
if "dairy_records" not in st.session_state:
    st.session_state.dairy_records = data.get("dairy_records", {})
if "last_reset_date" not in st.session_state:
    st.session_state.last_reset_date = data.get("last_reset_date", "")

# --- Daily Reset Handler ---
now = datetime.datetime.now()
today_date = now.date().isoformat()
if st.session_state.last_reset_date != today_date:
    st.session_state['duolingo_check_today'] = False
    st.session_state['morning_exercise_check_today'] = False
    st.session_state['jawline_check_today'] = False
    st.session_state.last_reset_date = today_date
    save_data()
else:
    if 'duolingo_check_today' not in st.session_state:
        st.session_state['duolingo_check_today'] = False
    if 'morning_exercise_check_today' not in st.session_state:
        st.session_state['morning_exercise_check_today'] = False
    if 'jawline_check_today' not in st.session_state:
        st.session_state['jawline_check_today'] = False

# --- Sidebar Navigation ---
st.sidebar.title("📘 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Afternoon Schedule",
    "DSA Sheet Scheduling",
    "Balanced Diet",
    "Mind & Body Routine",
    "Time Reminder",
    "Dairy",  # New
    "Details and Portfolio",
    "Stored Data",
    "App Update"
])
st.session_state.page = page

# --- Top Header ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"## 📅 Today's Date: {now.strftime('%A, %d %B %Y')}")
with col2:
    timer_placeholder = st.empty()

# --- Digital Clock ---
def update_clock():
    while True:
        clock = datetime.datetime.now().strftime("%H:%M:%S")
        timer_placeholder.markdown(
            f"<div style='text-align:right;font-size:20px;background:#000000;color:#39FF14;padding:8px;border-radius:8px;'>🕒 Timers: {clock}</div>",
            unsafe_allow_html=True
        )
        time.sleep(1)

thread = threading.Thread(target=update_clock)
thread.daemon = True
thread.start()

# --- Helper for Calendar Rendering ---
def render_activity_calendar(record_dict, year, month, title):
    month_cal = calendar.monthcalendar(year, month)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    tick = "<span style='color:green;font-size:22px;'>&#10003;</span>"
    cross = "<span style='color:red;font-size:22px;'>&#10007;</span>"

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
                day_date = datetime.date(year, month, day).isoformat()
                mark = tick if record_dict.get(day_date, False) else cross
                table_html += f"<td style='padding:7px'>{day}<br>{mark}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(f"##### {title}")
    st.markdown(table_html, unsafe_allow_html=True)
    
# --- Dairy calendar for selection and display ---
def render_dairy_calendar(dairy_records, year, month):
    # Month grid
    month_cal = calendar.monthcalendar(year, month)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    st.markdown("##### Division 4: Dairy Calendar")
    st.write("Click a date below to view its dairy entry.")
    # For interactivity, use buttons in a grid
    date_clicked = None
    grid = []
    for week in month_cal:
        row = []
        for day in week:
            if day == 0:
                row.append(st.empty())
            else:
                day_date = datetime.date(year, month, day).isoformat()
                if dairy_records.get(day_date):
                    # Entry exists
                    label = f"{day} 📝"
                    color = "white"
                    bg = "#39FF14"
                else:
                    label = str(day)
                    color = "#888"
                    bg = "#eee"
                row.append(st.button(label,
                                    key=f"dairycal_{year}{month}{day}",
                                    help="Show entry" if dairy_records.get(day_date) else "No entry",
                                    kwargs={'style':f"color:{color};background:{bg}"})
                )
        grid.append(row)
        
    # Position-wise manual callback
    day_found = None
    for wi, week in enumerate(month_cal):
        for di, day in enumerate(week):
            if day == 0:
                continue
            if st.session_state.get(f'dairycal_{year}{month}{day}', False):
                day_found = datetime.date(year, month, day).isoformat()
    return day_found

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

    # ========== 1. Morning Exercise ===========
    exc_col1, exc_col2 = st.columns([6,1])
    with exc_col1:
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
    with exc_col2:
        checked = st.checkbox("✔️ Completed", key=f"morning_exercise_check_{today_date}", value=st.session_state.get('morning_exercise_check_today', False))
        if 'morning_exercise_check_today' not in st.session_state or st.session_state['morning_exercise_check_today'] != checked:
            st.session_state['morning_exercise_check_today'] = checked
            st.session_state.morning_exercise_records[today_date] = checked
            save_data()

    # ========== 2. Jawline Routine ===========
    jaw_col1, jaw_col2 = st.columns([6,1])
    with jaw_col1:
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
    with jaw_col2:
        checked = st.checkbox("✔️ Completed", key=f"jawline_check_{today_date}", value=st.session_state.get('jawline_check_today', False))
        if 'jawline_check_today' not in st.session_state or st.session_state['jawline_check_today'] != checked:
            st.session_state['jawline_check_today'] = checked
            st.session_state.jawline_records[today_date] = checked
            save_data()

    # ========== 3. Duolingo Section ===========
    st.markdown("""
    <div style='background-color:#e6ffe6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>📘 DUOLINGO</h4>
    </div>
    """, unsafe_allow_html=True)
    duolingo_checked = st.checkbox("100 - 150 XP completed", key=f"duolingo_afternoon_{today_date}", value=st.session_state.get('duolingo_check_today', False))
    if 'duolingo_check_today' not in st.session_state or st.session_state['duolingo_check_today'] != duolingo_checked:
        st.session_state['duolingo_check_today'] = duolingo_checked
        st.session_state.duolingo_records[today_date] = duolingo_checked
        save_data()

    st.markdown("""<hr style='margin-top:35px;margin-bottom:10px;border:1px solid #ccc;'>""", unsafe_allow_html=True)
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

elif page == "Dairy":
    st.title("📖 Dairy Entry")
    st.markdown("Write your thoughts, experience, or a journal entry for today. (Saved per day, viewable later)")
    # Show today's saved value if it exists
    old_val = st.session_state.dairy_records.get(today_date, "")
    new_val = st.text_area("Your Dairy for Today:", value=old_val, height=350)
    if st.button("Save Dairy Entry"):
        st.session_state.dairy_records[today_date] = new_val
        save_data()
        st.success("Your dairy entry has been saved!")

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
    today = datetime.date.today()
    year, month = today.year, today.month

    # -- Division 1: Duolingo Checklist Calendar --
    render_activity_calendar(st.session_state.duolingo_records, year, month, "Division 1: Duolingo Activity Calendar")
    st.info("A green tick means Duolingo checklist was marked as completed for that day. A red cross means it was not done.")

    # -- Division 2: Morning Exercise Calendar --
    render_activity_calendar(st.session_state.morning_exercise_records, year, month, "Division 2: Morning Exercise Calendar")
    st.info("A green tick means Morning Exercise was marked completed for that day.")

    # -- Division 3: Jawline Routine Calendar --
    render_activity_calendar(st.session_state.jawline_records, year, month, "Division 3: Jawline Routine Calendar")
    st.info("A green tick means Jawline Routine was marked completed for that day.")

    # -- Division 4: Dairy Calendar --
    st.markdown("-----")
    st.markdown("#### Division 4: Dairy Calendar & Viewer")
    # Clickable calendar: show entry below when a day is clicked
    month_cal = calendar.monthcalendar(year, month)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    date_clicked = None
    cols = st.columns(7)
    with st.container():
        for idx, d in enumerate(days):
            cols[idx].markdown(f"**{d}**")
        for week in month_cal:
            row_cols = st.columns(7)
            for idx, day in enumerate(week):
                if day == 0:
                    row_cols[idx].markdown(" ")
                else:
                    day_date = datetime.date(year, month, day).isoformat()
                    label = str(day)
                    if st.session_state.dairy_records.get(day_date):
                        display = f"📝 {label}"
                    else:
                        display = label
                    if row_cols[idx].button(display, key=f"dairy_view_btn_{day_date}"):
                        date_clicked = day_date
    st.markdown("<small>📝: There's a dairy entry saved for this day.</small>", unsafe_allow_html=True)
    if date_clicked:
        entry = st.session_state.dairy_records.get(date_clicked, "")
        st.markdown(f"**Dairy Entry for {date_clicked}:**")
        if entry.strip():
            st.info(entry)
        else:
            st.warning("No dairy entry for this day.")

    # -- Division 5-6: Placeholders --
    for idx in range(5, 7):
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
