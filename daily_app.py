import streamlit as st
import pandas as pd
import datetime
from core.data_handler import save_data

def draw():
    st.title("🧠 DSA Sheet Scheduling")

    FIXED_KEYWORDS = ["CAT", "Gravitas"]
    today = datetime.date.today()

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
        save_data()

    def format_date_range(start, end):
        return f"{start.strftime('%b %d')} – {end.strftime('%b %d')}"

    def parse_start_date(date_range):
        try:
            date_str = date_range.split('–')[0].strip()
            return datetime.datetime.strptime(f"{date_str} 2025", "%b %d").date()
        except:
            return datetime.date(9999, 1, 1)

    def shift_schedule(topic, start, end, type_, note=""):
        days = (end - start).days + 1
        new_item = {"Type": type_, "Topic": topic, "Days": days, "Date Range": "", "Notes": note}
        schedule = sorted(st.session_state.dsa_sheet, key=lambda x: parse_start_date(x["Date Range"]))
        new_schedule = []
        inserted = False

        for entry in schedule:
            if not inserted and parse_start_date(entry["Date Range"]) >= start and not any(k.lower() in entry["Topic"].lower() for k in FIXED_KEYWORDS):
                new_schedule.append(new_item)
                inserted = True
            new_schedule.append(entry)

        if not inserted:
            new_schedule.append(new_item)

        recalculated = []
        cursor = start
        for item in new_schedule:
            if any(k.lower() in item["Topic"].lower() for k in FIXED_KEYWORDS):
                recalculated.append(item)
                cursor = parse_start_date(item["Date Range"]) + datetime.timedelta(days=item["Days"])
            else:
                item["Date Range"] = format_date_range(cursor, cursor + datetime.timedelta(days=item["Days"] - 1))
                recalculated.append(item)
                cursor += datetime.timedelta(days=item["Days"])

        for i, row in enumerate(recalculated):
            row["#"] = i + 1

        st.session_state.dsa_sheet = recalculated
        save_data()

    # 📋 Show table
    df = pd.DataFrame(st.session_state.dsa_sheet)

    def highlight_breaks(row):
        return ['background-color: #D0E7FF' if row.get("Type") == "Break" else "" for _ in row]

    st.markdown("### 📋 DSA Schedule with Notes (Editable)")
    st.dataframe(df.style.apply(highlight_breaks, axis=1), use_container_width=True)

    # 💾 Save notes
    if st.button("Save Notes"):
        for i in range(len(df)):
            st.session_state.dsa_sheet[i]["Notes"] = df.iloc[i]["Notes"]
        save_data()
        st.success("Notes saved!")

    # 🟩 Green Bar (Study)
    st.markdown("### 🟩 Add Study Topic")
    topic = st.text_input("Study Topic")
    col1, col2 = st.columns(2)
    from_date = col1.date_input("From Date", value=today, key="study_from")
    to_date = col2.date_input("To Date", value=today, key="study_to")
    if st.button("➕ Add Study"):
        if topic and from_date <= to_date:
            shift_schedule(topic, from_date, to_date, "DSA", note="✅ Manually Added")
            st.experimental_rerun()
        else:
            st.warning("Please enter a valid topic and date range.")

    # 🟥 Red Bar (Fun)
    st.markdown("### 🟥 Add Fun Activity")
    fun = st.text_input("Fun Activity")
    col3, col4 = st.columns(2)
    from_fun = col3.date_input("From Date", value=today, key="fun_from")
    to_fun = col4.date_input("To Date", value=today, key="fun_to")
    if st.button("➕ Add Fun"):
        if fun and from_fun <= to_fun:
            shift_schedule(fun, from_fun, to_fun, "Break", note="🎉 Fun")
            st.experimental_rerun()
        else:
            st.warning("Enter valid fun activity and dates.")

    # ⬜ Gray Bar (Wasted Time)
    st.markdown("### ⬜ Add Wasted Time")
    wasted = st.text_input("Reason for Wasted Time")
    col5, col6 = st.columns(2)
    from_waste = col5.date_input("From Date", value=today, key="waste_from")
    to_waste = col6.date_input("To Date", value=today, key="waste_to")
    if st.button("➕ Add Wasted"):
        if wasted and from_waste <= to_waste:
            shift_schedule(wasted, from_waste, to_waste, "Break", note="⚠️ Time Wasted")
            st.experimental_rerun()
        else:
            st.warning("Enter valid wasted time and range.")
