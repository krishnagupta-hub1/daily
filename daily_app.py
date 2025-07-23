import streamlit as st
import datetime
import threading
import time
import json
import os
import calendar
import pandas as pd

############### Date Utility ################
def get_today_date():
    return datetime.date.today().isoformat()

def get_now_datetime():
    return datetime.datetime.now()

def get_display_date():
    d = get_now_datetime()
    return d.strftime('%A, %d %B %Y')

############### Data Handling ################
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {
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
            "water_counts": st.session_state.water_counts,
            "water_checklists": st.session_state.water_checklists,
            "water_main_checklist": st.session_state.water_main_checklist,
            "passwords": st.session_state.passwords,
            "dsa_sheet": st.session_state.dsa_sheet,
            "important_dates": st.session_state.important_dates,
        }, f)

########### Session Init ################
data = load_data()
for key, default in [
    ("classroom_tasks", {
        "Database System": [],
        "Operating Systems": [],
        "Compiler Design": [],
        "Computer Networks": [],
        "Cloud Architecture Design": [],
    }),
    ("completed_classroom_tasks", {
        "Database System": {},
        "Operating Systems": {},
        "Compiler Design": {},
        "Computer Networks": {},
        "Cloud Architecture Design": {},
    }),
    ("app_updates", []),
    ("app_ideas", []),
    ("duolingo_records", {}),
    ("morning_exercise_records", {}),
    ("jawline_records", {}),
    ("dairy_records", {}),
    ("water_counts", {}),
    ("water_checklists", {}),
    ("water_main_checklist", {}),
    ("passwords", {
        "Folder 1": [],
        "Folder 2": [],
        "Folder 3": [],
        "Folder 4": [],
    }),
    ("dsa_sheet", [{} for _ in range(18)]),
    ("important_dates", []),
]:
    if key not in st.session_state:
        st.session_state[key] = data.get(key, default)

########### Sidebar Navigation #################
st.sidebar.title("📘 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Afternoon Schedule",
    "Classroom Studies",
    "DSA Sheet Scheduling",
    "Balanced Diet",
    "Mind & Body Routine",
    "Time Reminder",
    "Dairy",
    "Stored Data",
    "Important Dates",
    "Passwords",
    "Details and Portfolio",
    "App Update"
])

########### Top Header/Clock #################
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

########### Calendar Helpers #################
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

def render_classroom_calendar(completed_tasks_dict, year, month, title):
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
                has_any = any(completed_tasks_dict[subj].get(day_date) for subj in completed_tasks_dict)
                mark = tick if has_any else cross
                table_html += f"<td style='padding:7px'>{day}<br>{mark}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(f"##### {title}")
    st.markdown(table_html, unsafe_allow_html=True)

def render_water_calendar(water_main_checklist_dict, year, month, title):
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
                mark = tick if water_main_checklist_dict.get(day_date, False) else cross
                table_html += f"<td style='padding:7px'>{day}<br>{mark}</td>"
        table_html += "</tr>"
    table_html += "</table>"
    st.markdown(f"##### {title}")
    st.markdown(table_html, unsafe_allow_html=True)

########### Pages ###########################

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

elif page == "Afternoon Schedule":
    st.title("🕑 Afternoon Schedule")
    today_date = get_today_date()

    # 1. Morning Exercise
    exc_col1, exc_col2 = st.columns([6, 1])
    with exc_col1:
        st.markdown(
            """
            <div style='background-color:#f5f5f5;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
                <h4>🏃‍♂️ Morning 30 min Exercise</h4>
                <ul>
                    <li>Pushups 30</li>
                    <li>Crunches 30</li>
                    <li>Side planks or Russian twist 30</li>
                    <li>Bhujangasana 30 sec</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )
    with exc_col2:
        checked = st.checkbox("✔️ Completed", key=f"morning_exercise_check_{today_date}",
                              value=st.session_state.morning_exercise_records.get(today_date, False))
        if st.session_state.morning_exercise_records.get(today_date, False) != checked:
            st.session_state.morning_exercise_records[today_date] = checked
            save_data()

    # 2. Jawline Routine: with lips and eyes bullet points
    jaw_col1, jaw_col2 = st.columns([6, 1])
    with jaw_col1:
        st.markdown("""
        <div style='background-color:#ffe6e6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
            <h4>😁 Jawline Routine</h4>
            <div style='font-weight:bold; margin-bottom: 10px;'>25 min</div>
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
            <h5>4. Lips and Eyes:</h5>
            <ul>
                <li>Lips press</li>
                <li>Lip stretch</li>
                <li>Eyes movement in all directions</li>
            </ul>
            <p>5 min</p>
        </div>
        """, unsafe_allow_html=True)
    with jaw_col2:
        checked = st.checkbox("✔️ Completed", key=f"jawline_check_{today_date}",
                              value=st.session_state.jawline_records.get(today_date, False))
        if st.session_state.jawline_records.get(today_date, False) != checked:
            st.session_state.jawline_records[today_date] = checked
            save_data()

    # 3. Duolingo
    st.markdown("""
    <div style='background-color:#e6ffe6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>📘 DUOLINGO</h4>
    </div>
    """, unsafe_allow_html=True)
    duolingo_checked = st.checkbox("100 - 150 XP completed",
                                  key=f"duolingo_afternoon_{today_date}",
                                  value=st.session_state.duolingo_records.get(today_date, False))
    if st.session_state.duolingo_records.get(today_date, False) != duolingo_checked:
        st.session_state.duolingo_records[today_date] = duolingo_checked
        save_data()

    # 4. New Water Count 💧(AfC,L,E,D):
    st.markdown("""
    <div style='background-color:#ccf5ff;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>💧 Water Count (AfC,L,E,D):</h4>
    </div>
    """, unsafe_allow_html=True)

    water_count = st.number_input("Enter water count (0-4):", min_value=0, max_value=4, step=1,
                                   key=f"water_count_input_{today_date}",
                                   value=st.session_state.water_counts.get(today_date, 0))
    if st.session_state.water_counts.get(today_date, None) != water_count:
        st.session_state.water_counts[today_date] = water_count
        save_data()
    checklist_labels = ["AfC", "L", "E", "D"]
    cols = st.columns(4)
    checklist_states = st.session_state.water_checklists.get(today_date, [False, False, False, False])
    new_checklist_states = []
    for i in range(4):
        checked = cols[i].checkbox(checklist_labels[i], key=f"water_check_{today_date}_{i}", value=checklist_states[i])
        new_checklist_states.append(checked)
    if new_checklist_states != checklist_states:
        st.session_state.water_checklists[today_date] = new_checklist_states
        save_data()
    auto_checked = (water_count == 3 or water_count == 4)
    if auto_checked:
        st.info("Water Count is 3 or 4, consider marking at least 3 checklists.")
    small_checks_count = sum(new_checklist_states)
    big_check = small_checks_count >= 3
    prev_big_check = st.session_state.water_main_checklist.get(today_date, False)
    if prev_big_check != big_check:
        st.session_state.water_main_checklist[today_date] = big_check
        save_data()
    st.checkbox("✔️ Big Water Checklist", value=big_check, key=f"big_water_check_{today_date}", disabled=True)

    # 5. Classroom Studies with subject selection and 5 grids
    st.markdown("""<hr style='margin-top:30px;margin-bottom:10px;border:1px solid #ccc;'>""", unsafe_allow_html=True)
    st.markdown("<h3>📚 Classroom Studies</h3>", unsafe_allow_html=True)
    subjects = [
        "Database System",
        "Operating Systems",
        "Compiler Design",
        "Computer Networks",
        "Cloud Architecture Design"
    ]
    with st.form(key="classroom_studies_form_afternoon"):
        task = st.text_input("Enter your study topic:")
        date = st.date_input("Select the date for this task", value=datetime.date.today())
        selected_subject = st.selectbox("Select Subject", options=subjects)
        submitted = st.form_submit_button("Submit Study Task")
        if submitted:
            if task and selected_subject:
                st.session_state.classroom_tasks[selected_subject].append(
                    {"task": task.strip(), "date": str(date)}
                )
                save_data()
            else:
                st.warning("Please enter a task and select subject before submitting.")
    st.markdown("#### Pending Tasks (by subject)")
    grids = st.columns(5)
    for grid_idx, subject in enumerate(subjects):
        with grids[grid_idx]:
            st.markdown(f"<div style='background-color:#F6F8FA;padding:7px;border-radius:8px;font-weight:bold;text-align:center;'>{subject}</div>", unsafe_allow_html=True)
            to_remove = []
            for idx, task_item in enumerate(sorted(
                st.session_state.classroom_tasks[subject], key=lambda x: x["date"]
            )):
                key_done = f"classroom_done_{subject}_{idx}"
                if st.checkbox("Done", key=key_done):
                    date = task_item["date"]
                    if date not in st.session_state.completed_classroom_tasks[subject]:
                        st.session_state.completed_classroom_tasks[subject][date] = []
                    st.session_state.completed_classroom_tasks[subject][date].append(task_item["task"])
                    to_remove.append(idx)
                st.markdown(f"**{task_item['task']}**")
                st.write(f"📅 {task_item['date']}")
            if to_remove:
                for idx in sorted(to_remove, reverse=True):
                    st.session_state.classroom_tasks[subject].pop(idx)
                save_data()
                st.experimental_rerun()
            if not st.session_state.classroom_tasks[subject]:
                st.info("No pending tasks.")

elif page == "Classroom Studies":
    st.title("📚 Classroom Studies")
    st.info("This section moved to 'Afternoon Schedule' page.")

elif page == "Stored Data":
    st.title("🗃️ Stored Data")
    today = datetime.date.today()
    year, month = today.year, today.month

    # Division 1: Duolingo Calendar
    render_activity_calendar(st.session_state.duolingo_records, year, month, "Division 1: Duolingo Activity Calendar")
    st.info("A green tick means Duolingo checklist was marked as completed for that day.")

    # Division 2: Morning Exercise Calendar
    render_activity_calendar(st.session_state.morning_exercise_records, year, month, "Division 2: Morning Exercise Calendar")
    st.info("A green tick means Morning Exercise was marked completed.")

    # Division 3: Jawline Routine Calendar
    render_activity_calendar(st.session_state.jawline_records, year, month, "Division 3: Jawline Routine Calendar")
    st.info("A green tick means Jawline Routine was marked completed.")

    # Division 4: Classroom Studies Calendar
    render_classroom_calendar(st.session_state.completed_classroom_tasks, year, month, "Division 4: Classroom Studies Calendar")
    st.info("Click a ticked day (green tick) to view topics completed.")

    # Calendar with clickable days to show completed classroom studies by subject
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
                    found = False
                    for subject in st.session_state.completed_classroom_tasks:
                        if day_date in st.session_state.completed_classroom_tasks[subject]:
                            found = True
                            break
                    label = f"✅ {day}" if found else str(day)
                    if row_cols[idx].button(label, key=f"classroomcal_{day_date}"):
                        class_date_clicked = day_date
    if class_date_clicked:
        msgs = []
        for subject in st.session_state.completed_classroom_tasks:
            topics = st.session_state.completed_classroom_tasks[subject].get(class_date_clicked, [])
            if topics:
                msgs.append(f"**{subject}:** " + ", ".join(topics))
        if msgs:
            st.success("\n".join(msgs))
        else:
            st.warning("No classroom topics checked for this day.")

    # Division 5: Dairy Calendar (removed checklist, only normal calendar - click date to view or say not written)
    st.markdown("##### Dairy Calendar")
    selected_dairy_date = st.date_input("Select date to view Dairy Entry:", value=today)
    dairy_content = st.session_state.dairy_records.get(selected_dairy_date.isoformat(), None)
    if dairy_content:
        st.info(f"**Dairy for {selected_dairy_date}:** {dairy_content}")
    else:
        st.warning(f"Dairy was not written on {selected_dairy_date}.")

    # Division 6: Water Count Calendar (new)
    render_water_calendar(st.session_state.water_main_checklist, year, month, "Division 6: Water Count Calendar")
    st.info("A green tick means Big Water Checklist was marked completed for that day.")

    st.markdown(f"""<div style='background-color:#ffe6e6;padding:15px;border-radius:10px;margin-top:15px;margin-bottom:10px;'>
        <strong>Division 7:</strong> <span style='color:#888;'>[Your custom data or tracker here]</span>
    </div>""", unsafe_allow_html=True)

elif page == "DSA Sheet Scheduling":
    st.title("🧠 DSA Sheet Scheduling")

    # Define DSA schedule data
    dsa_schedule = [
        {"#":1, "Type":"DSA", "Topic":"Learn the Basics", "Days":7, "Date Range":"Jul 23 – Jul 29", "Notes":"–"},
        {"#":2, "Type":"DSA", "Topic":"Sorting Techniques", "Days":2, "Date Range":"Jul 30 – Jul 31", "Notes":"–"},
        {"#":3, "Type":"Break", "Topic":"— CAT-1 Break —", "Days":9, "Date Range":"Aug 17 – Aug 25", "Notes":"🟦 \"Topic cat-1\""},
        {"#":4, "Type":"DSA", "Topic":"Arrays", "Days":9, "Date Range":"Aug 1 – Aug 16 (✂️ split) + Aug 26", "Notes":"Continued after CAT-1"},
        {"#":5, "Type":"DSA", "Topic":"Binary Search", "Days":7, "Date Range":"Aug 27 – Sep 2", "Notes":"Shifted after CAT-1"},
        {"#":6, "Type":"Break", "Topic":"–", "Days":1, "Date Range":"Sep 3", "Notes":"Planned break"},
        {"#":7, "Type":"DSA", "Topic":"Strings", "Days":3, "Date Range":"Sep 4 – Sep 6", "Notes":"–"},
        {"#":8, "Type":"DSA", "Topic":"LinkedList", "Days":7, "Date Range":"Sep 7 – Sep 13", "Notes":"–"},
        {"#":9, "Type":"DSA", "Topic":"Recursion", "Days":6, "Date Range":"Sep 14 – Sep 19", "Notes":"–"},
        {"#":10, "Type":"Break", "Topic":"— Gravitas Prep —", "Days":3, "Date Range":"Sep 26 – Sep 28", "Notes":"🟦 \"Topic Gravitas\""},
        {"#":11, "Type":"DSA", "Topic":"Bit Manipulation", "Days":4, "Date Range":"Sep 20 – Sep 23", "Notes":"–"},
        {"#":12, "Type":"DSA", "Topic":"Stack & Queues", "Days":7, "Date Range":"Sep 24 – Sep 25 + Sep 29 – Oct 1", "Notes":"✂️ split by Gravitas"},
        {"#":13, "Type":"Break", "Topic":"— CAT-2 Break —", "Days":11, "Date Range":"Oct 2 – Oct 12", "Notes":"🟦 \"Topic cat 2\""},
        {"#":14, "Type":"DSA", "Topic":"Sliding Window / Two Pointer", "Days":3, "Date Range":"Oct 13 – Oct 15", "Notes":"Shifted post CAT-2"},
        {"#":15, "Type":"DSA", "Topic":"Heaps", "Days":4, "Date Range":"Oct 16 – Oct 19", "Notes":"–"},
        {"#":16, "Type":"DSA", "Topic":"Greedy", "Days":4, "Date Range":"Oct 20 – Oct 23", "Notes":"–"},
        {"#":17, "Type":"DSA", "Topic":"Binary Trees", "Days":9, "Date Range":"Oct 24 – Nov 1", "Notes":"–"},
        {"#":18, "Type":"Break", "Topic":"–", "Days":1, "Date Range":"Nov 2", "Notes":"Planned break"},
        {"#":19, "Type":"DSA", "Topic":"Binary Search Trees", "Days":4, "Date Range":"Nov 3 – Nov 6", "Notes":"–"},
        {"#":20, "Type":"DSA", "Topic":"Graphs", "Days":12, "Date Range":"Nov 7 – Nov 18", "Notes":"–"},
        {"#":21, "Type":"Break", "Topic":"–", "Days":1, "Date Range":"Nov 19", "Notes":"Planned break"},
        {"#":22, "Type":"DSA", "Topic":"Dynamic Programming", "Days":13, "Date Range":"Nov 20 – Dec 2", "Notes":"–"},
        {"#":23, "Type":"Break", "Topic":"–", "Days":1, "Date Range":"Dec 3", "Notes":"Planned break"},
        {"#":24, "Type":"DSA", "Topic":"Tries", "Days":2, "Date Range":"Dec 4 – Dec 5", "Notes":"–"},
        {"#":25, "Type":"DSA", "Topic":"Strings (Adv)", "Days":3, "Date Range":"Dec 6 – Dec 8", "Notes":"–"}
    ]

    # Parse the date range's start date to a sortable datetime for ordering
    def parse_start_date(date_range):
        # Extract first date part before any special chars or splits
        first_part = date_range.split('+')[0].split('(')[0].strip()
        # Dates are in format e.g. Jul 23 – Jul 29 or Sep 3 — or single date
        # When only one date, parse directly
        parts = first_part.split('–')
        start_str = parts[0].strip()
        try:
            # Append year 2025 (assumed based on current date)
            dt = datetime.datetime.strptime(f"{start_str} 2025", "%b %d %Y")
        except:
            dt = datetime.datetime.max  # fallback to max
        return dt

    # Sort by start date
    dsa_schedule_sorted = sorted(dsa_schedule, key=lambda x: parse_start_date(x["Date Range"]))

    # Create DataFrame for display & editing notes
    df = pd.DataFrame(dsa_schedule_sorted)

    # Editable Notes column only
    edited_notes = []
    for i, row in df.iterrows():
        key = f"dsa_notes_edit_{row['#']}"
        val = st.text_input(f"Notes for #{row['#']} {row['Topic']}", value=row["Notes"], key=key)
        edited_notes.append(val)
    df["Notes"] = edited_notes

    # Create a styled table with blue background for breaks rows
    def highlight_breaks(row):
        bg_color = '#D0E7FF' if row['Type'] == 'Break' else ''
        return ['background-color: {}'.format(bg_color)]*len(row)
    st.markdown("### DSA Schedule with Notes (Editable)")
    st.dataframe(df.style.apply(highlight_breaks, axis=1))

    # Save Notes back to session state on button click
    if st.button("Save Notes"):
        # Update the underlying data structure with edited notes
        for i, row in df.iterrows():
            for item in st.session_state.dsa_sheet:
                # Match by number and topic and update notes if found
                if ('#' in item and item['#']==row['#']) or ('topic' in item and row['Topic'].startswith(item.get('topic',''))):
                    item['notes'] = row['Notes']
                    break
        # Persist notes changes for next reload
        save_data()
        st.success("Notes saved successfully!")


elif page == "Important Dates":
    st.title("📅 Important Dates")
    with st.form(key="important_dates_form"):
        topic = st.text_input("Enter important topic/description:")
        imp_date = st.date_input("Select date for topic:", value=datetime.date.today())
        submitted = st.form_submit_button("Add Important Date")
        if submitted and topic:
            st.session_state.important_dates.append({"topic": topic.strip(), "date": imp_date.isoformat()})
            st.session_state.important_dates = sorted(st.session_state.important_dates, key=lambda x: x["date"])
            save_data()
    st.markdown("### Saved Important Dates")
    for entry in st.session_state.important_dates:
        st.markdown(f"<div style='background:#F8F2FC;border-radius:8px;padding:7px;margin-bottom:4px;'><b>{entry['date']}</b>: {entry['topic']}</div>", unsafe_allow_html=True)

elif page == "Passwords":
    st.title("🔒 Password Vault")
    folders = ["Folder 1", "Folder 2", "Folder 3", "Folder 4"]
    with st.form(key="passwords_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        content = st.text_input("Content/Description")
        dest_folder = st.selectbox("Push to folder:", options=folders)
        submitted = st.form_submit_button("Push to Folder (Green Button)")
        if submitted and username and password and content and dest_folder:
            st.session_state.passwords[dest_folder].append({
                "username": username,
                "password": password,
                "content": content
            })
            save_data()
            st.success(f"Saved to {dest_folder}.")
    pw_cols = st.columns(4)
    for idx, folder in enumerate(folders):
        with pw_cols[idx]:
            st.markdown(f"<div style='background:#EDF4FF;border-radius:8px;padding:7px;text-align:center;font-weight:bold;'>{folder}</div>", unsafe_allow_html=True)
            for entry in st.session_state.passwords[folder]:
                st.markdown(f"<div style='background:#E8ECF1;border-radius:8px;padding:7px;margin:6px 0 6px 0;'>"
                            f"Content: {entry['content']}<br>Username: {entry['username']}<br>Password: {entry['password']}</div>", unsafe_allow_html=True)

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
    today_date = get_today_date()
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
