import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta

# ---------- Constants ----------
BREAKS = [
    {"Topic": "CAT-1", "From": "2025-08-14", "To": "2025-08-25"},
    {"Topic": "Gravitas", "From": "2025-09-25", "To": "2025-09-29"},
    {"Topic": "CAT-2", "From": "2025-10-02", "To": "2025-10-13"},
    {"Topic": "Diwali Travel 1", "From": "2025-10-17", "To": "2025-10-18"},
    {"Topic": "Diwali Travel 2", "From": "2025-10-26", "To": "2025-10-27"},
    {"Topic": "FAT & Labs", "From": "2025-11-06", "To": "2025-12-06"},
]

FIXED_BREAK_DF = pd.DataFrame([
    {"S.No.": f"#P{i+1}", "Topic": b["Topic"], "From": b["From"], "To": b["To"], "Type": "Break"} for i, b in enumerate(BREAKS)
])

DSA_TOPICS = [
    ("Arrays Part-1", 2), ("Arrays Part-2", 1), ("Arrays Part-3", 1),
    ("Binary Search-1", 2), ("Binary Search-2", 1), ("Binary Search-3", 2),
    ("Recursion-1", 1), ("Recursion-2", 1), ("Recursion-3", 1),
    ("Linked List-1", 2), ("Linked List-2", 2), ("Linked List-3", 2),
]

# ---------- Helper Functions ----------
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def is_break_day(date):
    for _, row in FIXED_BREAK_DF.iterrows():
        if row["From"] <= date.strftime("%Y-%m-%d") <= row["To"]:
            return True
    return False

def add_days_skipping_breaks(start_date, days):
    current = start_date
    added = 0
    while added < days:
        current += timedelta(days=1)
        if not is_break_day(current):
            added += 1
    return current

def rebuild_schedule(start_date, inserted_rows):
    schedule = []
    current_date = start_date
    serial = 1

    all_inserted = pd.concat([FIXED_BREAK_DF, inserted_rows], ignore_index=True)
    all_inserted["From"] = pd.to_datetime(all_inserted["From"])
    all_inserted = all_inserted.sort_values("From")

    topic_index = 0
    while topic_index < len(DSA_TOPICS):
        topic, days = DSA_TOPICS[topic_index]
        end_date = add_days_skipping_breaks(current_date, days - 1)

        overlap_found = False
        for _, row in all_inserted.iterrows():
            row_start = row["From"]
            row_end = pd.to_datetime(row["To"])
            if row_start <= end_date and current_date <= row_end:
                overlap_found = True
                overlap_days = (row_start - current_date).days
                if overlap_days > 0:
                    part1_end = current_date + timedelta(days=overlap_days - 1)
                    schedule.append({"S.No.": f"{serial}.1", "Topic": f"{topic} (Part 1)", "From": current_date.strftime("%Y-%m-%d"), "To": part1_end.strftime("%Y-%m-%d"), "Type": "DSA"})
                    serial += 1
                    days -= overlap_days
                current_date = row_end + timedelta(days=1)
                break

        if not overlap_found:
            schedule.append({"S.No.": str(serial), "Topic": topic, "From": current_date.strftime("%Y-%m-%d"), "To": end_date.strftime("%Y-%m-%d"), "Type": "DSA"})
            serial += 1
            current_date = end_date + timedelta(days=1)
            topic_index += 1

    final_df = pd.concat([inserted_rows, FIXED_BREAK_DF, pd.DataFrame(schedule)], ignore_index=True)
    final_df = final_df.sort_values("From").reset_index(drop=True)
    return final_df

# ---------- Streamlit Page Logic ----------
def draw():
    st.title("📅 DSA Schedule with Notes")

    if "inserted_rows" not in st.session_state:
        st.session_state.inserted_rows = pd.DataFrame(columns=["S.No.", "Topic", "From", "To", "Type"])

    today = datetime.date.today()
    schedule_df = rebuild_schedule(today, st.session_state.inserted_rows)

    st.dataframe(schedule_df, hide_index=True, use_container_width=True)

    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        topic = st.text_input("Add DSA Topic (Green)", key="green_topic")
    with col2:
        from_date = st.date_input("From", key="green_from")
    with col3:
        to_date = st.date_input("To", key="green_to")
    with col4:
        if st.button("Go ✅", key="green_go"):
            new_row = {"S.No.": f"U{len(st.session_state.inserted_rows)+1}", "Topic": topic, "From": str(from_date), "To": str(to_date), "Type": "User"}
            st.session_state.inserted_rows = pd.concat([st.session_state.inserted_rows, pd.DataFrame([new_row])], ignore_index=True)
            st.rerun()

    st.markdown("---")

    st.subheader("🗑️ Delete a Row")
    if len(st.session_state.inserted_rows) > 0:
        delete_index = st.number_input("Enter Row Index to Delete (0-based)", min_value=0, max_value=len(st.session_state.inserted_rows)-1, step=1)
        if st.button("Delete Row"):
            st.session_state.inserted_rows.drop(index=delete_index, inplace=True)
            st.session_state.inserted_rows.reset_index(drop=True, inplace=True)
            st.rerun()

    st.markdown("---")

# ---------- Main Entry ----------
def main():
    draw()

if __name__ == "__main__":
    main()
