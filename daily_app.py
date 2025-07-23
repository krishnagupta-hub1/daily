import streamlit as st
import datetime
import threading
import time
import json
import os
import calendar

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
    st.markdown("### DSA Progress Sheet")
    dsa_topics = [
        "Step 1 : Learn the basics 0 / 31",
        "Step 2 : Learn Important Sorting Techniques 0 / 7",
        "Step 3 : Solve Problems on Arrays [Easy → Medium → Hard] 0 / 40",
        "Step 4 : Binary Search [1D, 2D Arrays, Search Space] 0 / 32",
        "Step 5 : Strings [Basic and Medium] 0 / 15",
        "Step 6 : Learn LinkedList [Single LL, Double LL, Medium, Hard Problems] 0 / 31",
        "Step 7 : Recursion [PatternWise] 0 / 25",
        "Step 8 : Bit Manipulation [Concepts & Problems] 0 / 18",
        "Step 9 : Stack and Queues [Learning, Pre-In-Post-fix, Monotonic Stack, Implementation] 0 / 30",
        "Step 10 : Sliding Window & Two Pointer Combined Problems 0 / 12",
        "Step 11 : Heaps [Learning, Medium, Hard Problems] 0 / 17",
        "Step 12 : Greedy Algorithms [Easy, Medium/Hard] 0 / 16",
        "Step 13 : Binary Trees [Traversals, Medium and Hard Problems] 0 / 39",
        "Step 14 : Binary Search Trees [Concept and Problems] 0 / 16",
        "Step 15 : Graphs [Concepts & Problems] 0 / 54",
        "Step 16 : Dynamic Programming [Patterns and Problems] 0 / 56",
        "Step 17 : Tries 0 / 7",
        "Step 18 : Strings 0 / 9"
    ]
    if "dsa_sheet" not in st.session_state or len(st.session_state.dsa_sheet) != 18:
        st.session_state.dsa_sheet = [{} for _ in range(18)]
    dsa_sheet_changed = False
    with st.form(key="dsa_sheet_form"):
        sheet_rows = []
        for i, topic in enumerate(dsa_topics):
            if not st.session_state.dsa_sheet[i]:
                st.session_state.dsa_sheet[i] = {"topic": topic, "completed_date": "", "days_taken": "", "unable_days": ""}
            col1, col2, col3, col4, col5 = st.columns([1,5,2,2,2])
            col1.write(str(i+1))
            col2.write(topic)
            completed_date = col3.text_input("", value=st.session_state.dsa_sheet[i].get("completed_date", ""), key=f"dsa_compdate_{i}")
            days_taken = col4.text_input("", value=st.session_state.dsa_sheet[i].get("days_taken", ""), key=f"dsa_days_{i}")
            unable_days = col5.text_input("", value=st.session_state.dsa_sheet[i].get("unable_days", ""), key=f"dsa_unable_{i}")
            if completed_date != st.session_state.dsa_sheet[i].get("completed_date") or \
               days_taken != st.session_state.dsa_sheet[i].get("days_taken") or \
               unable_days != st.session_state.dsa_sheet[i].get("unable_days"):
                st.session_state.dsa_sheet[i]["completed_date"] = completed_date
                st.session_state.dsa_sheet[i]["days_taken"] = days_taken
                st.session_state.dsa_sheet[i]["unable_days"] = unable_days
                dsa_sheet_changed = True
        if st.form_submit_button("Save DSA Sheet"):
            if dsa_sheet_changed:
                save_data()
            st.success("DSA Sheet saved successfully!")

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
