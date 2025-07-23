import streamlit as st
import calendar
import datetime
from core.calendar_helpers import (
    render_activity_calendar, render_classroom_calendar, render_water_calendar
)

def draw():
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
