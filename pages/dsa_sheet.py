#dsa.py 

import streamlit as st
import pandas as pd
import datetime
from core.data_handler import save_data

def draw():
    st.title("🧠 DSA Sheet Scheduling")

    FIXED_KEYWORDS = ["CAT", "Gravitas"]
    today = datetime.date.today()

    # If not initialized
    if "dsa_sheet" not in st.session_state or not isinstance(st.session_state.dsa_sheet, list):
        st.session_state.dsa_sheet = []

    # --- Helper to parse Date Range start ----
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

    # --- Update Schedule with Entry ---
    def insert_and_shift_schedule(name, start, end, type_, note=""):
        new_days = (end - start).days + 1

        inserted = {
            "Type": type_,
            "Topic": name,
            "Days": new_days,
            "Date Range": format_date_range(start, end),
            "Notes": note or "–"
        }

        # Sort existing schedule
        sorted_schedule = sorted(
            st.session_state.dsa_sheet,
            key=lambda x: parse_start_date(x["Date Range"])
        )

        new_schedule = []
        inserted_flag = False

        for row in sorted_schedule:
            is_fixed = any(kw.lower() in row["Topic"].lower() for kw in FIXED_KEYWORDS)

            if not inserted_flag and parse_start_date(row["Date Range"]).date() >= start:
                new_schedule.append(inserted)
                inserted_flag = True

            new_schedule.append(row)

        if not inserted_flag:
            new_schedule.append(inserted)

        # Recalculate Dates (skip fixed)
        recalculated = []
        cursor = start
        for item in new_schedule:
            is_fixed = any(kw.lower() in item["Topic"].lower() for kw in FIXED_KEYWORDS)
            days = item.get("Days", 1)

            if is_fixed:
                recalculated.append(item)
                cursor = parse_start_date(item["Date Range"]).date() + datetime.timedelta(days=item["Days"])
                continue

            start_dt = cursor
            end_dt = cursor + datetime.timedelta(days=days - 1)
            item["Date Range"] = format_date_range(start_dt, end_dt)
            cursor = end_dt + datetime.timedelta(days=1)
            recalculated.append(item)

        # Re-number and save
        for idx, task in enumerate(recalculated):
            task["#"] = idx + 1

        st.session_state.dsa_sheet = recalculated
        save_data()

    # ------------------ TABLE DISPLAY -------------------
    df = pd.DataFrame(st.session_state.dsa_sheet)

    if not df.empty:
        def highlight_breaks(row):
            return ['background-color: #D0E7FF' if row['Type'] == 'Break' else '' for _ in row]
        st.markdown("### DSA Schedule with Notes (Editable)")
        st.dataframe(df.style.apply(highlight_breaks, axis=1), use_container_width=True)
    else:
        st.info("No DSA entries found yet. Add one using options below.")

    # ------------------ SAVE NOTES -------------------
    if df.shape[0] > 0:
        if st.button("💾 Save Notes"):
            for i, row in df.iterrows():
                st.session_state.dsa_sheet[i]["Notes"] = row["Notes"]
            save_data()
            st.success("Notes saved successfully!")

    # -------------- INPUT BARS BELOW ------------------

    # 🟩 GREEN BAR – Study Topic Done
    st.markdown("<div style='background:#e9ffe9;padding:15px;margin-top:10px;border-radius:8px;'>"
                "<h4>🟩 Add Study (Green Bar)</h4>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    green_topic = g1.text_input("Topic You Studied / Completed", key="green_topic")
    green_from = g2.date_input("From", key="green_from", value=today)
    green_to = g2.date_input("Till", key="green_to", value=today+datetime.timedelta(days=1))
    if st.button("➕ GO - Add Study"):
        if green_topic and green_from <= green_to:
            insert_and_shift_schedule(green_topic, green_from, green_to, "DSA", note="✅ Manually Added")
            st.success(f"Added topic: {green_topic}")
            st.experimental_rerun()
        else:
            st.warning("Check topic and date range!")

    # 🟥 RED BAR – Fun Break
    st.markdown("<div style='background:#ffeaea;padding:15px;margin-top:10px;border-radius:8px;'>"
                "<h4>🟥 Add Fun Activity (Red Bar)</h4>", unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    red_topic = r1.text_input("Fun You Did (e.g. Movie, Sports)", key="red_topic")
    red_from = r2.date_input("From", key="red_from", value=today)
    red_to = r2.date_input("Till", key="red_to", value=today+datetime.timedelta(days=1))
    if st.button("➕ GO - Add Fun"):
        if red_topic and red_from <= red_to:
            insert_and_shift_schedule(red_topic, red_from, red_to, "Break", note="🎈 Fun/Enjoyment")
            st.success(f"Added fun: {red_topic}")
            st.experimental_rerun()
        else:
            st.warning("Please enter fun topic and valid date range.")

    # ⬜ GRAY BAR – Wasted Time
    st.markdown("<div style='background:#f0f0f0;padding:15px;margin-top:10px;border-radius:8px;'>"
                "<h4>⬜ Add Wasted Time (Gray Bar)</h4>", unsafe_allow_html=True)
    y1, y2 = st.columns(2)
    gray_reason = y1.text_input("Wasted Time Reason", key="gray_reason")
    gray_from = y2.date_input("From", key="gray_from", value=today)
    gray_to = y2.date_input("Till", key="gray_to", value=today+datetime.timedelta(days=1))
    if st.button("➕ GO - Add Wasted Time"):
        if gray_reason and gray_from <= gray_to:
            insert_and_shift_schedule(gray_reason, gray_from, gray_to, "Break", note="😓 Time Wasted")
            st.success(f"Logged wasted time: {gray_reason}")
            st.experimental_rerun()
        else:
            st.warning("Please enter a reason and date range.")


