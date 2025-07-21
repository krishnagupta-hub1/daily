import streamlit as st
import datetime
import time
import threading
import json
import os
import calendar

def get_today_date():
    return datetime.date.today().isoformat()

def get_now_datetime():
    return datetime.datetime.now()

def get_display_date():
    d = get_now_datetime()
    return d.strftime('%A, %d %B %Y')

st.set_page_config(layout="wide", page_title="Daily Tracker")

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
        "dairy_records": {},
        "coding_study_todo": {},       # {"2025-07-22": [list of tasks], ...}
        "coding_study_done": {}        # {"2025-07-22": [list of completed tasks], ...}
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
            "coding_study_todo": st.session_state.coding_study_todo,
            "coding_study_done": st.session_state.coding_study_done
        }, f)

data = load_data()
for key, default in [
    ("classroom_tasks", []),
    ("app_updates", []),
    ("app_ideas", []),
    ("duolingo_records", {}),
    ("morning_exercise_records", {}),
    ("jawline_records", {}),
    ("dairy_records", {}),
    ("coding_study_todo", {}),
    ("coding_study_done", {})
]:
    if key not in st.session_state:
        st.session_state[key] = data.get(key, default)

st.sidebar.title("📘 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Afternoon Schedule",
    "Coding Study",
    "DSA Sheet Scheduling",
    "Balanced Diet",
    "Mind & Body Routine",
    "Time Reminder",
    "Dairy",
    "Details and Portfolio",
    "Stored Data",
    "App Update"
])

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

def render_coding_calendar(coding_done_dict, year, month, title):
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
                completed = bool(coding_done_dict.get(day_date, []))
                mark = tick if completed else cross
                table_html += f"<td style='padding:7px'>{day}<br>{mark}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(f"##### {title}")
    st.markdown(table_html, unsafe_allow_html=True)

if page == "Coding Study":
    st.title("💻 Coding Study To-Do List")
    today_date = get_today_date()
    # --- Input new coding study tasks ---
    if today_date not in st.session_state.coding_study_todo:
        st.session_state.coding_study_todo[today_date] = []
    if today_date not in st.session_state.coding_study_done:
        st.session_state.coding_study_done[today_date] = []
    new_task = st.text_input("Add Coding Study Task (DSA, LeetCode, Project, etc.) for today:")
    if st.button("Add Coding Task"):
        if new_task.strip():
            st.session_state.coding_study_todo[today_date].append(new_task.strip())
            save_data()
        else:
            st.warning("Please enter some task")

    # --- Show today's to-do, each with a checklist ---
    st.markdown("#### Today's Coding To-Do")
    if st.session_state.coding_study_todo[today_date]:
        for idx, task in enumerate(st.session_state.coding_study_todo[today_date]):
            col1, col2 = st.columns([7,1])
            with col1:
                st.write(task)
            with col2:
                if st.checkbox("Done", key=f"coding_done_{today_date}_{idx}"):
                    # Move to 'done' for today
                    st.session_state.coding_study_done[today_date].append(task)
                    st.session_state.coding_study_todo[today_date].pop(idx)
                    save_data()
                    st.experimental_rerun()
    else:
        st.info("No coding tasks left for today! Add more above.")

    # --- Show completed for today ---
    if st.session_state.coding_study_done[today_date]:
        st.success(
            "**Done today:**\n- " +
            "\n- ".join(st.session_state.coding_study_done[today_date])
        )

elif page == "Stored Data":
    st.title("🗃️ Stored Data")
    today = datetime.date.today()
    year, month = today.year, today.month

    # -- 1: Duolingo --
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

    render_activity_calendar(st.session_state.duolingo_records, year, month, "Division 1: Duolingo Activity Calendar")
    st.info("A green tick means Duolingo checklist was marked as completed for that day.")

    # -- 2: Morning Exercise --
    render_activity_calendar(st.session_state.morning_exercise_records, year, month, "Division 2: Morning Exercise Calendar")
    st.info("A green tick means Morning Exercise was marked completed.")

    # -- 3: Jawline Routine --
    render_activity_calendar(st.session_state.jawline_records, year, month, "Division 3: Jawline Routine Calendar")
    st.info("A green tick means Jawline Routine was marked completed.")

    # -- 4: Coding Study Calendar with clickable days, show done entries --
    st.markdown("-----")
    render_coding_calendar(st.session_state.coding_study_done, year, month, "Division 4: Coding Study Calendar")
    st.info("Click a completed day below (green tick) to view the tasks completed.")

    # Interactive calendar: click days to display that day's coding study content if any
    month_cal = calendar.monthcalendar(year, month)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    st.markdown("##### View Coding Study Done")
    code_date_clicked = None
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
                    done_today = st.session_state.coding_study_done.get(day_date, [])
                    style_color = "#39FF14" if done_today else "#eee"
                    label = f"✅ {day}" if done_today else str(day)
                    if row_cols[idx].button(label, key=f"codingcal_{day_date}"):
                        code_date_clicked = day_date
    if code_date_clicked:
        cdone = st.session_state.coding_study_done.get(code_date_clicked, [])
        if cdone:
            st.success("**Done on " + code_date_clicked + ":**\n- " + "\n- ".join(cdone))
        else:
            st.warning("No coding study was checked for this day.")

    # -- 5: Dairy Calendar and Viewer --
    st.markdown("-----")
    st.markdown("#### Division 5: Dairy Calendar & Viewer")
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

    # -- 6: Placeholder --
    st.markdown(f"""<div style='background-color:#ffe6e6;padding:15px;border-radius:10px;margin-top:15px;margin-bottom:10px;'>
        <strong>Division 6:</strong> <span style='color:#888;'>[Your custom data or tracker here]</span>
    </div>""", unsafe_allow_html=True)

# The remainder of your code for Home, Afternoon Schedule, DSA, Dairy etc remains unchanged from previous
# (for brevity, not repeated here since no changes needed except in Coding Study and Stored Data)

# ... (include all other sections as already adapted above)
