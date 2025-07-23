import streamlit as st
import datetime
from core.date_utils import get_today_date
from core.data_handler import save_data

def draw():
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
    jaw_col1, jaw_col2 = st.columns([6,1])
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

    # 4. New Water Count 💧 (AfC,L,E,D)
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
