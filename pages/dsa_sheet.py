import streamlit as st
import pandas as pd
import datetime
from core.data_handler import save_data

def draw():
    st.title("🧠 DSA Sheet Scheduling")

    FIXED_KEYWORDS = ["CAT", "Gravitas"]
    today = datetime.date.today()

    # --- Initial default schedule rows ---
    INITIAL_SCHEDULE = [
        {"#": 1, "Type": "DSA", "Topic": "Learn the Basics", "Days": 7, "Date Range": "Jul 23 – Jul 29", "Notes": "–"},
        {"#": 2, "Type": "DSA", "Topic": "Sorting Techniques", "Days": 2, "Date Range": "Jul 30 – Jul 31", "Notes": "–"},
        {"#": 3, "Type": "Break", "Topic": "— CAT-1 Break —", "Days": 9, "Date Range": "Aug 17 – Aug 25", "Notes": "🟦 \"Topic cat-1\""},
        {"#": 4, "Type": "DSA", "Topic": "Arrays", "Days": 9, "Date Range": "Aug 1 – Aug 16 (✂️ split) + Aug 26", "Notes": "Continued after CAT-1"},
        {"#": 5, "Type": "DSA", "Topic": "Binary Search", "Days": 7, "Date Range": "Aug 27 – Sep 2", "Notes": "Shifted after CAT-1"},
        {"#": 6, "Type": "Break", "Topic": "–", "Days": 1, "Date Range": "Sep 3", "Notes": "Planned break"},
        {"#": 7, "Type": "DSA", "Topic": "Strings", "Days": 3, "Date Range": "Sep 4 – Sep 6", "Notes": "–"},
        {"#": 8, "Type": "DSA", "Topic": "LinkedList", "Days": 7, "Date Range": "Sep 7 – Sep 13", "Notes": "–"},
        {"#": 9, "Type": "DSA", "Topic": "Recursion", "Days": 6, "Date Range": "Sep 14 – Sep 19", "Notes": "–"},
        {"#": 10, "Type": "Break", "Topic": "— Gravitas Prep —", "Days": 3, "Date Range": "Sep 26 – Sep 28", "Notes": "🟦 \"Topic Gravitas\""},
        {"#": 11, "Type": "DSA", "Topic": "Bit Manipulation", "Days": 4, "Date Range": "Sep 20 – Sep 23", "Notes": "–"},
        {"#": 12, "Type": "DSA", "Topic": "Stack & Queues", "Days": 7, "Date Range": "Sep 24 – Sep 25 + Sep 29 – Oct 1", "Notes": "✂️ split by Gravitas"},
        {"#": 13, "Type": "Break", "Topic": "— CAT-2 Break —", "Days": 11, "Date Range": "Oct 2 – Oct 12", "Notes": "🟦 \"Topic cat 2\""},
        {"#": 14, "Type": "DSA", "Topic": "Sliding Window / Two Pointer", "Days": 3, "Date Range": "Oct 13 – Oct 15", "Notes": "Shifted post CAT-2"},
        {"#": 15, "Type": "DSA", "Topic": "Heaps", "Days": 4, "Date Range": "Oct 16 – Oct 19", "Notes": "–"},
        {"#": 16, "Type": "DSA", "Topic": "Greedy", "Days": 4, "Date Range": "Oct 20 – Oct 23", "Notes": "–"},
        {"#": 17, "Type": "DSA", "Topic": "Binary Trees", "Days": 9, "Date Range": "Oct 24 – Nov 1", "Notes": "–"},
        {"#": 18, "Type": "Break", "Topic": "–", "Days": 1, "Date Range": "Nov 2", "Notes": "Planned break"},
        {"#": 19, "Type": "DSA", "Topic": "Binary Search Trees", "Days": 4, "Date Range": "Nov 3 – Nov 6", "Notes": "–"},
        {"#": 20, "Type": "DSA", "Topic": "Graphs", "Days": 12, "Date Range": "Nov 7 – Nov 18", "Notes": "–"},
        {"#": 21, "Type": "Break", "Topic": "–", "Days": 1, "Date Range": "Nov 19", "Notes": "Planned break"},
        {"#": 22, "Type": "DSA", "Topic": "Dynamic Programming", "Days": 13, "Date Range": "Nov 20 – Dec 2", "Notes": "–"},
        {"#": 23, "Type": "Break", "Topic": "–", "Days": 1, "Date Range": "Dec 3", "Notes": "Planned break"},
        {"#": 24, "Type": "DSA", "Topic": "Tries", "Days": 2, "Date Range": "Dec 4 – Dec 5", "Notes": "–"},
        {"#": 25, "Type": "DSA", "Topic": "Strings (Adv)", "Days": 3, "Date Range": "Dec 6 – Dec 8", "Notes": "–"},
    ]

    if "dsa_sheet" not in st.session_state or not st.session_state.dsa_sheet:
        st.session_state.dsa_sheet = INITIAL_SCHEDULE.copy()
        save_data()  # 🔁 Save immediately so it's persistent

    def format_date_range(start, end):
        return f"{start.strftime('%b %d')} – {end.strftime('%b %d')}"

    def parse_start_date(date_range):
        first_part = date_range.split('+')[0].split('(')[0].strip()
        parts = first_part.split('–')
        start_str = parts[0].strip()
        try:
            return datetime.datetime.strptime(f"{start_str} 2025", "%b %d %Y").date()
        except:
            return datetime.date(9999, 1, 1)

    def shift_schedule(new_topic, start, end, type_, note=""):
        new_days = (end - start).days + 1
        new_entry = {
            "Type": type_,
            "Topic": new_topic,
            "Days": new_days,
            "Date Range": format_date_range(start, end),
            "Notes": note
        }

        new_sched = []
        inserted = False

        sorted_sched = sorted(st.session_state.dsa_sheet, key=lambda x: parse_start_date(x["Date Range"]))
        for item in sorted_sched:
            is_fixed = any(k.lower() in item["Topic"].lower() for k in FIXED_KEYWORDS)
            if not inserted and parse_start_date(item["Date Range"]) >= start:
                new_sched.append(new_entry)
                inserted = True
            new_sched.append(item)
        if not inserted:
            new_sched.append(new_entry)

        recalculated = []
        cursor = start
        for item in new_sched:
            is_fixed = any(k.lower() in item["Topic"].lower() for k in FIXED_KEYWORDS)
            if is_fixed:
                recalculated.append(item)
                cursor = parse_start_date(item["Date Range"]) + datetime.timedelta(days=item["Days"])
                continue
            item["Date Range"] = format_date_range(cursor, cursor + datetime.timedelta(days=item["Days"] - 1))
            recalculated.append(item)
            cursor += datetime.timedelta(days=item["Days"])

        for i, item in enumerate(recalculated):
            item["#"] = i + 1

        st.session_state.dsa_sheet = recalculated
        save_data()

    # --- TABLE DISPLAY ---
    df = pd.DataFrame(st.session_state.dsa_sheet)
    st.markdown("### 📋 DSA Schedule with Notes (Editable)")
    st.dataframe(df.style.apply(lambda row: ['background-color: #D0E7FF' if row['Type'] == 'Break' else '' for _ in row], axis=1), use_container_width=True)

    if st.button("💾 Save Notes"):
        for i, row in df.iterrows():
            st.session_state.dsa_sheet[i]["Notes"] = row["Notes"]
        save_data()
        st.success("Notes saved!")

    # --- GREEN BAR ---
    st.markdown("<div style='background:#e9ffe9;padding:15px;margin-top:15px;border-radius:8px;'><h4>🟩 Add Study Topic</h4></div>", unsafe_allow_html=True)
    topic = st.text_input("Topic", key="green_topic")
    from_dt = st.date_input("From", key="green_from", value=today)
    to_dt = st.date_input("Till", key="green_to", value=today)
    if st.button("➕ Add Study", key="add_green"):
        if topic and from_dt <= to_dt:
            shift_schedule(topic, from_dt, to_dt, "DSA", note="✅ Manually Added")
            st.experimental_rerun()

    # --- RED BAR ---
    st.markdown("<div style='background:#ffeaea;padding:15px;margin-top:15px;border-radius:8px;'><h4>🟥 Add Fun Activity</h4></div>", unsafe_allow_html=True)
    fun = st.text_input("Fun You Did", key="red_topic")
    from_dt2 = st.date_input("From", key="red_from", value=today)
    to_dt2 = st.date_input("Till", key="red_to", value=today)
    if st.button("➕ Add Fun", key="add_red"):
        if fun and from_dt2 <= to_dt2:
            shift_schedule(fun, from_dt2, to_dt2, "Break", note="🎉 Fun")
            st.experimental_rerun()

    # --- GRAY BAR ---
    st.markdown("<div style='background:#f0f0f0;padding:15px;margin-top:15px;border-radius:8px;'><h4>⬜ Add Wasted Time</h4></div>", unsafe_allow_html=True)
    waste = st.text_input("Time Wasted Reason", key="gray_reason")
    from_dt3 = st.date_input("From", key="gray_from", value=today)
    to_dt3 = st.date_input("Till", key="gray_to", value=today)
    if st.button("➕ Add Waste", key="add_gray"):
        if waste and from_dt3 <= to_dt3:
            shift_schedule(waste, from_dt3, to_dt3, "Break", note="⚠️ Wasted Time")
            st.experimental_rerun()







