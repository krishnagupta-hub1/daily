import streamlit as st
import pandas as pd
import datetime

st.set_page_config(layout="wide")

# Title
st.title("🧠 DSA Sheet Scheduling")

# Original schedule data
def load_schedule():
    return [
        {"#": 1, "Type": "DSA", "Topic": "Learn the Basics", "Days": 7, "Date Range": "Jul 23 – Jul 29", "Notes": "–"},
        {"#": 2, "Type": "DSA", "Topic": "Sorting Techniques", "Days": 2, "Date Range": "Jul 30 – Jul 31", "Notes": "–"},
        {"#": 4, "Type": "DSA", "Topic": "Arrays", "Days": 9, "Date Range": "Aug 1 – Aug 16 (✂ split) + Aug 26", "Notes": "Continued after CAT-1"},
        {"#": 3, "Type": "Break", "Topic": "— CAT-1 Break —", "Days": 9, "Date Range": "Aug 17 – Aug 25", "Notes": "🟦 \"Topic cat-1\""},
        {"#": 5, "Type": "DSA", "Topic": "Binary Search", "Days": 7, "Date Range": "Aug 27 – Sep 2", "Notes": "Shifted after CAT-1"},
        {"#": 6, "Type": "Break", "Topic": "–", "Days": 1, "Date Range": "Sep 3", "Notes": "Planned break"},
        {"#": 7, "Type": "DSA", "Topic": "Strings", "Days": 3, "Date Range": "Sep 4 – Sep 6", "Notes": "–"},
        {"#": 8, "Type": "DSA", "Topic": "LinkedList", "Days": 7, "Date Range": "Sep 7 – Sep 13", "Notes": "–"},
        {"#": 9, "Type": "DSA", "Topic": "Recursion", "Days": 6, "Date Range": "Sep 14 – Sep 19", "Notes": "–"},
        {"#": 11, "Type": "DSA", "Topic": "Bit Manipulation", "Days": 4, "Date Range": "Sep 20 – Sep 23", "Notes": "–"},
        {"#": 10, "Type": "Break", "Topic": "— Gravitas Prep —", "Days": 3, "Date Range": "Sep 26 – Sep 28", "Notes": "🟦 \"Topic Gravitas\""},
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
        {"#": 25, "Type": "DSA", "Topic": "Strings (Adv)", "Days": 3, "Date Range": "Dec 6 – Dec 8", "Notes": "–"}
    ]

def parse_date(s):
    return datetime.datetime.strptime(s + ' 2025', '%b %d %Y')

def highlight_breaks(row):
    color = '#D0E7FF' if row['Type'] == 'Break' else ''
    return ['background-color: {}'.format(color)] * len(row)

# Load and display the initial table
schedule = load_schedule()
df = pd.DataFrame(schedule)
st.markdown("### DSA Schedule Table")
st.dataframe(df.style.apply(highlight_breaks, axis=1), use_container_width=True)

# Custom Insert Section
st.markdown("---")
st.markdown("### 🟩 Green Bar (Topic Work Done)")
with st.container():
    g_topic = st.text_input("Topic")
    g_from = st.date_input("From Date", key="g_from")
    g_to = st.date_input("Till Date", key="g_to")
    if st.button("Go Green"):
        st.success(f"Green Bar: {g_topic} from {g_from} to {g_to}")

st.markdown("### 🟥 Red Bar (Fun Time)")
with st.container():
    r_fun = st.text_input("Fun you did")
    r_from = st.date_input("From Date", key="r_from")
    r_to = st.date_input("Till Date", key="r_to")
    if st.button("Go Red"):
        st.success(f"Red Bar: {r_fun} from {r_from} to {r_to}")

st.markdown("### ⬜ Gray Bar (Time Wasted)")
with st.container():
    y_reason = st.text_input("Reason for waste")
    y_from = st.date_input("From Date", key="y_from")
    y_to = st.date_input("Till Date", key="y_to")
    if st.button("Go Gray"):
        st.success(f"Gray Bar: {y_reason} from {y_from} to {y_to}")






