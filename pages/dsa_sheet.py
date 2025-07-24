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

    # Initialize session state once
    if "dsa_sheet" not in st.session_state or not st.session_state.dsa_sheet:
        st.session_state.dsa_sheet = INITIAL_SCHEDULE.copy()

    def parse_start_date(date_range):
        first_part = date_range.split("+")[0].split("(")[0].strip()
        parts = first_part.split("–")
        start_str = parts[0].strip()
        try:
            dt = datetime.datetime.strptime(f"{start_str} 2025", "%b %d %Y")
            return dt.date()
        except Exception:
            return None

    def format_date_range(start, end):
        return f"{start.strftime('%b %d')} – {end.strftime('%b %d')}"

    def insert_and_shift_schedule(name, start, end, type_, note=""):
        new_days = (end - start).days + 1
        new_item = {
            "Type": type_,
            "Topic": name,
            "Days": new_days,
            "Date Range": format_date_range(start, end),
            "Notes": note or "–",
        }

        # Sort current schedule by start date
        current = sorted(st.session_state.dsa_sheet, key=lambda x: parse_start_date(x["Date Range"]) or datetime.date(9999,1,1))

        new_schedule = []
        inserted = False

        for item in current:
            is_fixed = any(kw.lower() in item["Topic"].lower() for kw in FIXED_KEYWORDS)

            if not inserted and parse_start_date(item["Date Range"]) and parse_start_date(item["Date Range"]) >= start:
                new_schedule.append(new_item)
                inserted = True
            new_schedule.append(item)

        if not inserted:
            new_schedule.append(new_item)

        # Recalculate dates
        recalculated = []
        cursor = start
        for item in new_schedule:
            is_fixed = any(kw.lower() in item["Topic"].lower() for kw in FIXED_KEYWORDS)
            days = item.get("Days", 1)

            if is_fixed:
                recalculated.append(item)
                fixed_start = parse_start_date(item["Date Range"])
                if fixed_start is None:
                    fixed_start = cursor
                cursor = fixed_start + datetime.timedelta(days=days)
                continue

            item["Date Range"] = format_date_range(cursor, cursor + datetime.timedelta(days=days -1))
            cursor += datetime.timedelta(days=days)
            recalculated.append(item)

        for idx, task in enumerate(recalculated):
            task["#"] = idx + 1

        st.session_state.dsa_sheet = recalculated
        save_data()

    # Show table with editable notes
    df = pd.DataFrame(st.session_state.dsa_sheet)

    if not df.empty:
        def highlight_breaks(row):
            return ['background-color: #D0E7FF' if row['Type'] == 'Break' else '' for _ in row]
        st.markdown("### DSA Schedule with Notes (Editable)")
        st.dataframe(df.style.apply(highlight_breaks, axis=1), use_container_width=True)
    else:
        st.info("No DSA entries found yet. Add one using options below.")

    # Save notes button
    if df.shape[0] > 0:
        if st.button("💾 Save Notes"):
            for i, row in df.iterrows():
                st.session_state.dsa_sheet[i]["Notes"] = row["Notes"]
            save_data()
            st.success("Notes saved successfully!")

    # Three input bars beneath the table

    # --- Green Bar: Study Topic ---
    st.markdown("<div style='background:#e9ffe9;padding:15px;margin-top:15px;border-radius:8px;'>"
                "<h4>🟩 Add Study Topic</h4></div>", unsafe_allow_html=True)
    g_col1, g_col2 = st.columns(2)
    green_topic = g_col1.text_input("Topic You Studied / Completed", key="green_topic_input")
    green_from = g_col2.date_input("From Date", key="green_from_date", value=today)
    green_to = g_col2.date_input("Till Date", key="green_to_date", value=today)
    if st.button("➕ GO - Add Study Topic", key="green_add_button"):
        if green_topic and green_from <= green_to:
            insert_and_shift_schedule(green_topic, green_from, green_to, "DSA", note="✅ Manually Added")
            st.success(f"Added study topic: {green_topic}")
            st.experimental_rerun()
        else:
            st.warning("Please enter a valid topic and date range.")

    # --- Red Bar: Fun Activity ---
    st.markdown("<div style='background:#ffeaea;padding:15px;margin-top:15px;border-radius:8px;'>"
                "<h4>🟥 Add Fun Activity</h4></div>", unsafe_allow_html=True)
    r_col1, r_col2 = st.columns(2)
    red_topic = r_col1.text_input("Fun You Did (e.g. Movie, Sports)", key="red_topic_input")
    red_from = r_col2.date_input("From Date", key="red_from_date", value=today)
    red_to = r_col2.date_input("Till Date", key="red_to_date", value=today)
    if st.button("➕ GO - Add Fun Activity", key="red_add_button"):
        if red_topic and red_from <= red_to:
            insert_and_shift_schedule(red_topic, red_from, red_to, "Break", note="🎈 Fun/Enjoyment")
            st.success(f"Added fun activity: {red_topic}")
            st.experimental_rerun()
        else:
            st.warning("Please enter a valid fun activity and date range.")

    # --- Gray Bar: Wasted Time ---
    st.markdown("<div style='background:#f0f0f0;padding:15px;margin-top:15px;border-radius:8px;'>"
                "<h4>⬜ Add Wasted Time</h4></div>", unsafe_allow_html=True)
    y_col1, y_col2 = st.columns(2)
    gray_reason = y_col1.text_input("Wasted Time Reason", key="gray_reason_input")
    gray_from = y_col2.date_input("From Date", key="gray_from_date", value=today)
    gray_to = y_col2.date_input("Till Date", key="gray_to_date", value=today)
    if st.button("➕ GO - Add Wasted Time", key="gray_add_button"):
        if gray_reason and gray_from <= gray_to:
            insert_and_shift_schedule(gray_reason, gray_from, gray_to, "Break", note="😓 Time Wasted")
            st.success(f"Logged wasted time: {gray_reason}")
            st.experimental_rerun()
        else:
            st.warning("Please enter a valid reason and date range.")





