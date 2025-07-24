import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout="wide")
st.title("🧠 DSA Sheet Scheduling")

# -----------------------------------
# DSA Data (Original)
# -----------------------------------

original_schedule = [
    {"#": 1, "Type": "DSA", "Topic": "Learn the Basics", "Days": 7, "Date Range": "Jul 23 – Jul 29", "Notes": "–"},
    {"#": 2, "Type": "DSA", "Topic": "Sorting Techniques", "Days": 2, "Date Range": "Jul 30 – Jul 31", "Notes": "–"},
    {"#": 3, "Type": "DSA", "Topic": "Arrays", "Days": 9, "Date Range": "Aug 1 – Aug 16 (✂ split) + Aug 26", "Notes": "Continued after CAT-1"},
    {"#": 4, "Type": "Break", "Topic": "— CAT-1 Break —", "Days": 9, "Date Range": "Aug 17 – Aug 25", "Notes": "🟦 \"Topic cat-1\""},
    {"#": 5, "Type": "DSA", "Topic": "Binary Search", "Days": 7, "Date Range": "Aug 27 – Sep 2", "Notes": "Shifted after CAT-1"},
    {"#": 6, "Type": "Break", "Topic": "–", "Days": 1, "Date Range": "Sep 3", "Notes": "Planned break"},
    {"#": 7, "Type": "DSA", "Topic": "Strings", "Days": 3, "Date Range": "Sep 4 – Sep 6", "Notes": "–"},
    {"#": 8, "Type": "DSA", "Topic": "LinkedList", "Days": 7, "Date Range": "Sep 7 – Sep 13", "Notes": "–"},
    {"#": 9, "Type": "DSA", "Topic": "Recursion", "Days": 6, "Date Range": "Sep 14 – Sep 19", "Notes": "–"},
    {"#": 10, "Type": "DSA", "Topic": "Bit Manipulation", "Days": 4, "Date Range": "Sep 20 – Sep 23", "Notes": "–"},
    {"#": 11, "Type": "Break", "Topic": "— Gravitas Prep —", "Days": 3, "Date Range": "Sep 26 – Sep 28", "Notes": "🟦 \"Topic Gravitas\""},
    {"#": 12, "Type": "DSA", "Topic": "Stack & Queues", "Days": 7, "Date Range": "Sep 24 – Sep 25 + Sep 29 – Oct 1", "Notes": "✂ split by Gravitas"},
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

# -----------------------------------
# Helper Functions
# -----------------------------------

def parse_start_date(date_range):
    first_part = date_range.split('+')[0].split('(')[0].strip()
    start_str = first_part.split('–')[0].strip()
    try:
        return datetime.datetime.strptime(f"{start_str} 2025", "%b %d %Y")
    except:
        return datetime.datetime.max

def highlight_breaks(row):
    return ['background-color: #D0E7FF' if row['Type'] == 'Break' else '' for _ in row]

def is_conflict(date, fixed_ranges):
    return any(start <= date <= end for (start, end) in fixed_ranges)

def get_fixed_date_ranges(schedule):
    ranges = []
    for item in schedule:
        if item['Type'] == 'Break':
            dr = item['Date Range']
            start, end = [d.strip() for d in dr.replace('–', '-').split('-')]
            try:
                s_date = datetime.datetime.strptime(start + " 2025", "%b %d %Y")
                e_date = datetime.datetime.strptime(end + " 2025", "%b %d %Y")
                ranges.append((s_date, e_date))
            except:
                continue
    return ranges

# -----------------------------------
# DSA Table Display
# -----------------------------------

df = pd.DataFrame(original_schedule)
df_sorted = df.sort_values(by="Date Range", key=lambda col: col.map(parse_start_date))
st.markdown("### 📅 DSA Schedule with Notes (Editable)")
st.dataframe(df_sorted.style.apply(highlight_breaks, axis=1), use_container_width=True)

# -----------------------------------
# Input Sections (Green, Red, Gray)
# -----------------------------------

def insert_custom_event(color: str):
    st.markdown(f"#### ➕ {color.capitalize()} Bar Input")
    with st.form(f"{color}_form"):
        topic = st.text_input(f"{color.capitalize()} Topic")
        reason = st.text_input("Reason / Fun Description")
        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From Date", key=f"{color}_from")
        with col2:
            till_date = st.date_input("Till Date", key=f"{color}_to")
        submitted = st.form_submit_button("GO")
        if submitted and from_date and till_date and topic:
            st.success(f"{color.capitalize()} task added: {topic} from {from_date} to {till_date}")
            # Actual event insertion logic would go here

# Three colored bars
insert_custom_event("green")
insert_custom_event("red")
insert_custom_event("gray")










