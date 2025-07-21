import streamlit as st
import datetime
import threading
import time
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

def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {
        "classroom_tasks": [],
        "completed_classroom_tasks": {},  # new: {date: [task, ...]}
        "app_updates": [],
        "app_ideas": [],
        "duolingo_records": {},
        "morning_exercise_records": {},
        "jawline_records": {},
        "dairy_records": {},
        "coding_study_todo": {},
        "coding_study_done": {}
    }

def save_data():
    with open("data.json", "w") as f:
        json.dump({
            "classroom_tasks": st.session_state.classroom_tasks,
            "completed_classroom_tasks": st.session_state.completed_classroom_tasks,
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
    ("completed_classroom_tasks", {}),
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
    "DSA Sheet Scheduling",
    "Balanced Diet",
    "Mind & Body Routine",
    "Time Reminder",
    "Classroom Studies",  # Include Classroom Studies as its own section
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

def render_classroom_calendar(classroom_done_dict, year, month, title):
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
                completed = bool(classroom_done_dict.get(day_date, []))
                mark = tick if completed else cross
                table_html += f"<td style='padding:7px'>{day}<br>{mark}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(f"##### {title}")
    st.markdown(table_html, unsafe_allow_html=True)

############## Classroom Studies Section ##############
if page == "Classroom Studies":
    st.title("📚 Classroom Studies (with To-Do & Calendar Movement)")
    # Input for new task
    with st.form(key="classroom_studies_form"):
        task = st.text_input("Enter your study topic:")
        date = st.date_input("Select the date for this task", value=datetime.date.today())
        submitted = st.form_submit_button("Submit Study Task")
        if submitted:
            if task:
                st.session_state.classroom_tasks.append((task.strip(), str(date)))
                save_data()
            else:
                st.warning("Please enter a task before submitting.")

    # Show tasks -- sort by date ascending, then show done checklist beside
    st.markdown("#### Pending Tasks (sortable by date)")
    sorted_tasks = sorted(
        [(i, t, d) for i, (t, d) in enumerate(st.session_state.classroom_tasks)],
        key=lambda x: x[2]
    )
    to_remove = []
    for idx, task, date in sorted_tasks:
        col1, col2, col3 = st.columns([6,3,1])
        with col1:
            st.write(f"**{task}**")
        with col2:
            st.write(f"📅 {date}")
        with col3:
            if st.checkbox("Done", key=f"classroom_done_{idx}"):
                # Move to completed for that date
                if date not in st.session_state.completed_classroom_tasks:
                    st.session_state.completed_classroom_tasks[date] = []
                st.session_state.completed_classroom_tasks[date].append(task)
                to_remove.append(idx)
    if to_remove:
        # Remove in reverse to keep indices correct
        for idx in sorted(to_remove, reverse=True):
            st.session_state.classroom_tasks.pop(idx)
        save_data()
        st.experimental_rerun()
    if not sorted_tasks:
        st.info("No pending classroom studies! Add more tasks above.")

    # Show completed today (optional, for quick reference)
    today_date = get_today_date()
    if st.session_state.completed_classroom_tasks.get(today_date, []):
        st.success("**Done today:**\n- " + "\n- ".join(st.session_state.completed_classroom_tasks[today_date]))

############### Stored Data Calendars Section ################
elif page == "Stored Data":
    st.title("🗃️ Stored Data")
    today = datetime.date.today()
    year, month = today.year, today.month

    render_activity_calendar(st.session_state.duolingo_records, year, month, "Division 1: Duolingo Activity Calendar")
    st.info("A green tick means Duolingo checklist was marked as completed for that day.")

    render_activity_calendar(st.session_state.morning_exercise_records, year, month, "Division 2: Morning Exercise Calendar")
    st.info("A green tick means Morning Exercise was marked completed.")

    render_activity_calendar(st.session_state.jawline_records, year, month, "Division 3: Jawline Routine Calendar")
    st.info("A green tick means Jawline Routine was marked completed.")

    # ----- Classroom Calendar (Division 4) -----
    render_classroom_calendar(st.session_state.completed_classroom_tasks, year, month, "Division 4: Classroom Studies Calendar")
    st.info("Green tick if any classroom topic was checked done on that day. Click a ticked day to view.")

    # Calendar with clickable days to show completed classroom studies details
    month_cal = calendar.monthcalendar(year, month)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    st.markdown("##### View Classroom Studies Done")
    class_date_clicked = None
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
                    done_today = st.session_state.completed_classroom_tasks.get(day_date, [])
                    label = f"✅ {day}" if done_today else str(day)
                    if row_cols[idx].button(label, key=f"classroomcal_{day_date}"):
                        class_date_clicked = day_date
    if class_date_clicked:
        done_topics = st.session_state.completed_classroom_tasks.get(class_date_clicked, [])
        if done_topics:
            st.success("**Done on " + class_date_clicked + ":**\n- " + "\n- ".join(done_topics))
        else:
            st.warning("No classroom topics checked for this day.")

    # --- Rest of the divisions: Dairy and placeholders ---
    render_activity_calendar(st.session_state.dairy_records, year, month, "Division 5: Dairy Calendar")
    st.markdown(f"""<div style='background-color:#ffe6e6;padding:15px;border-radius:10px;margin-top:15px;margin-bottom:10px;'>
        <strong>Division 6:</strong> <span style='color:#888;'>[Your custom data or tracker here]</span>
    </div>""", unsafe_allow_html=True)

########## (The rest of your sections: Afternoon, DSA, Dairy, etc) #####################
# ... Unchanged from prior versions unless you want more changes ...
# Copy here from your previous code to preserve all features.

