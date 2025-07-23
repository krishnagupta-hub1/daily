import streamlit as st
import pandas as pd
import datetime
from core.data_handler import save_data

def draw():
    st.title("🧠 DSA Sheet Scheduling")

    fixed_keywords = ["CAT", "Gravitas"]
    today = datetime.date.today()
    
    # Load sheet or initialize
    if not st.session_state.dsa_sheet or not isinstance(st.session_state.dsa_sheet, list):
        st.session_state.dsa_sheet = []

    def parse_start_date(date_range):
        first_part = date_range.split('+')[0].split('(')[0].strip()
        parts = first_part.split('–')
        start_str = parts[0].strip()
        try:
            dt = datetime.datetime.strptime(f"{start_str} 2025", "%b %d %Y")
        except:
            dt = datetime.datetime.max
        return dt

    def format_date_range(start, end):
        return f"{start.strftime('%b %d')} – {end.strftime('%b %d')}"

    def add_entry_to_schedule(entry_topic, days, start_date, end_date, label_type, note="-"):
        new_entry = {
            "#": len(st.session_state.dsa_sheet) + 1,
            "Type": label_type,
            "Topic": entry_topic,
            "Days": days,
            "Date Range": format_date_range(start_date, end_date),
            "Notes": note
        }

        # Step 1: Insert at right spot
        new_list = []
        inserted = False
        for item in st.session_state.dsa_sheet:
            # Determine if this item is fixed break
            fixed = any(kw.lower() in item.get("Topic", "").lower() for kw in fixed_keywords)
            if not inserted and parse_start_date(item.get("Date Range", "Dec 31")) >= datetime.datetime.combine(start_date, datetime.time()):
                # Insert before this only if not during fixed block
                new_list.append(new_entry)
                inserted = True
            new_list.append(item)

        if not inserted:
            new_list.append(new_entry)

        # Step 2: Recalculate future dates, but DO NOT shift fixed blocks
        recalculated = []
        cursor = new_list[0:1]
        cursor_date = start_date
        for task in new_list:
            is_fixed = any(kw.lower() in task["Topic"].lower() for kw in fixed_keywords)
            if is_fixed:
                recalculated.append(task)
                cursor_date = parse_start_date(task["Date Range"]).date() + datetime.timedelta(days=task["Days"])
                continue
            days = task["Days"]
            start = cursor_date
            end = start + datetime.timedelta(days=days - 1)
            task["Date Range"] = format_date_range(start, end)
            cursor_date = end + datetime.timedelta(days=1)
            recalculated.append(task)

        # Update session
        for idx, task in enumerate(recalculated):
            task["#"] = idx + 1

        st.session_state.dsa_sheet = recalculated
        save_data()

    # ------------------ Data Table -------------------
    df = pd.DataFrame(st.session_state.dsa_sheet)
    if not df.empty:
        def highlight_breaks(row):
            bg_color = '#D0E7FF' if row['Type'] == 'Break' else ''
            return ['background-color: {}'.format(bg_color)]*len(row)
        st.markdown("### DSA Schedule with Notes (Editable)")
        st.dataframe(df.style.apply(highlight_breaks, axis=1), use_container_width=True)
    else:
        st.info("No entries in your DSA sheet yet. Add one below.")

    # ----------------- Save Notes ----------------------
    if df.shape[0] > 0 and "Notes" in df.columns:
        st.markdown(" ")
        if st.button("Save Notes"):
            for i, row in df.iterrows():
                task = st.session_state.dsa_sheet[i]
                if "Notes" in row:
                    task["Notes"] = row["Notes"]
            save_data()
            st.success("Notes saved successfully!")

    # ----------------- Green Bar ----------------------
    st.markdown("<div style='background:#e6ffe6;padding:15px;margin-top:15px;border-radius:8px;'><h4>🟩 Add Study Topic</h4>", unsafe_allow_html=True)
    green_topic = st.text_input("✅ Topic Completed", key="green_topic")
    g_col1, g_col2 = st.columns(2)
    green_from = g_col1.date_input("From Date", value=today, key="green_from")
    green_to = g_col2.date_input("Till Date", value=today, key="green_to")
    if st.button("GO - Green Bar"):
        if green_topic and green_from <= green_to:
            delta = (green_to - green_from).days + 1
            add_entry_to_schedule(green_topic, delta, green_from, green_to, "DSA")
            st.success("✅ Study topic added to schedule.")
            st.experimental_rerun()
        else:
            st.warning("Please enter a valid topic and date range.")

    # ----------------- Red Bar ----------------------
    st.markdown("<div style='background:#ffd2d2;padding:15px;margin-top:10px;border-radius:8px;'><h4>🟥 Add Fun Break</h4>", unsafe_allow_html=True)
    red_fun = st.text_input("🎉 Fun you did (Movie/Sport/Social)", key="red_fun")
    r_col1, r_col2 = st.columns(2)
    red_from = r_col1.date_input("From Date", value=today, key="red_from")
    red_to = r_col2.date_input("Till Date", value=today, key="red_to")
    if st.button("GO - Red Bar"):
        if red_fun and red_from <= red_to:
            delta = (red_to - red_from).days + 1
            add_entry_to_schedule(red_fun, delta, red_from, red_to, "Break", note="🎉 Fun Activity")
            st.success("🎉 Fun entry added to schedule.")
            st.experimental_rerun()
        else:
            st.warning("Please enter valid fun activity and date range.")

    # ----------------- Gray Bar ----------------------
    st.markdown("<div style='background:#f0f0f0;padding:15px;margin-top:10px;border-radius:8px;'><h4>⬜ Add Wasted Reason</h4>", unsafe_allow_html=True)
    gray_reason = st.text_input("🙁 Time Wasted Reason", key="gray_reason")
    y_col1, y_col2 = st.columns(2)
    gray_from = y_col1.date_input("From Date", value=today, key="gray_from")
    gray_to = y_col2.date_input("Till Date", value=today, key="gray_to")
    if st.button("GO - Gray Bar"):
        if gray_reason and gray_from <= gray_to:
            delta = (gray_to - gray_from).days + 1
            add_entry_to_schedule(gray_reason, delta, gray_from, gray_to, "Break", note="🚫 Time Wasted")
            st.success("🚫 Time-waste entry added to schedule.")
            st.experimental_rerun()
        else:
            st.warning("Please enter valid reason and date range.")

