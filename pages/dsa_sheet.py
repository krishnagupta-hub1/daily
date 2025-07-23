import streamlit as st
import pandas as pd
import datetime

def draw():
    st.title("🧠 DSA Sheet Scheduling")

    # Define DSA schedule data
    dsa_schedule = [
        {"#":1, "Type":"DSA", "Topic":"Learn the Basics", "Days":7, "Date Range":"Jul 23 – Jul 29", "Notes":"–"},
        {"#":2, "Type":"DSA", "Topic":"Sorting Techniques", "Days":2, "Date Range":"Jul 30 – Jul 31", "Notes":"–"},
        {"#":3, "Type":"Break", "Topic":"— CAT-1 Break —", "Days":9, "Date Range":"Aug 17 – Aug 25", "Notes":"🟦 \"Topic cat-1\""},
        {"#":4, "Type":"DSA", "Topic":"Arrays", "Days":9, "Date Range":"Aug 1 – Aug 16 (✂️ split) + Aug 26", "Notes":"Continued after CAT-1"},
        {"#":5, "Type":"DSA", "Topic":"Binary Search", "Days":7, "Date Range":"Aug 27 – Sep 2", "Notes":"Shifted after CAT-1"},
        {"#":6, "Type":"Break", "Topic":"–", "Days":1, "Date Range":"Sep 3", "Notes":"Planned break"},
        {"#":7, "Type":"DSA", "Topic":"Strings", "Days":3, "Date Range":"Sep 4 – Sep 6", "Notes":"–"},
        {"#":8, "Type":"DSA", "Topic":"LinkedList", "Days":7, "Date Range":"Sep 7 – Sep 13", "Notes":"–"},
        {"#":9, "Type":"DSA", "Topic":"Recursion", "Days":6, "Date Range":"Sep 14 – Sep 19", "Notes":"–"},
        {"#":10, "Type":"Break", "Topic":"— Gravitas Prep —", "Days":3, "Date Range":"Sep 26 – Sep 28", "Notes":"🟦 \"Topic Gravitas\""},
        {"#":11, "Type":"DSA", "Topic":"Bit Manipulation", "Days":4, "Date Range":"Sep 20 – Sep 23", "Notes":"–"},
        {"#":12, "Type":"DSA", "Topic":"Stack & Queues", "Days":7, "Date Range":"Sep 24 – Sep 25 + Sep 29 – Oct 1", "Notes":"✂️ split by Gravitas"},
        {"#":13, "Type":"Break", "Topic":"— CAT-2 Break —", "Days":11, "Date Range":"Oct 2 – Oct 12", "Notes":"🟦 \"Topic cat 2\""},
        {"#":14, "Type":"DSA", "Topic":"Sliding Window / Two Pointer", "Days":3, "Date Range":"Oct 13 – Oct 15", "Notes":"Shifted post CAT-2"},
        {"#":15, "Type":"DSA", "Topic":"Heaps", "Days":4, "Date Range":"Oct 16 – Oct 19", "Notes":"–"},
        {"#":16, "Type":"DSA", "Topic":"Greedy", "Days":4, "Date Range":"Oct 20 – Oct 23", "Notes":"–"},
        {"#":17, "Type":"DSA", "Topic":"Binary Trees", "Days":9, "Date Range":"Oct 24 – Nov 1", "Notes":"–"},
        {"#":18, "Type":"Break", "Topic":"–", "Days":1, "Date Range":"Nov 2", "Notes":"Planned break"},
        {"#":19, "Type":"DSA", "Topic":"Binary Search Trees", "Days":4, "Date Range":"Nov 3 – Nov 6", "Notes":"–"},
        {"#":20, "Type":"DSA", "Topic":"Graphs", "Days":12, "Date Range":"Nov 7 – Nov 18", "Notes":"–"},
        {"#":21, "Type":"Break", "Topic":"–", "Days":1, "Date Range":"Nov 19", "Notes":"Planned break"},
        {"#":22, "Type":"DSA", "Topic":"Dynamic Programming", "Days":13, "Date Range":"Nov 20 – Dec 2", "Notes":"–"},
        {"#":23, "Type":"Break", "Topic":"–", "Days":1, "Date Range":"Dec 3", "Notes":"Planned break"},
        {"#":24, "Type":"DSA", "Topic":"Tries", "Days":2, "Date Range":"Dec 4 – Dec 5", "Notes":"–"},
        {"#":25, "Type":"DSA", "Topic":"Strings (Adv)", "Days":3, "Date Range":"Dec 6 – Dec 8", "Notes":"–"}
    ]

    def parse_start_date(date_range):
        first_part = date_range.split('+')[0].split('(')[0].strip()
        parts = first_part.split('–')
        start_str = parts[0].strip()
        try:
            dt = datetime.datetime.strptime(f"{start_str} 2025", "%b %d %Y")
        except:
            dt = datetime.datetime.max  # fallback
        return dt

    dsa_schedule_sorted = sorted(dsa_schedule, key=lambda x: parse_start_date(x["Date Range"]))

    df = pd.DataFrame(dsa_schedule_sorted)

    # Editable notes handling
    edited_notes = []
    for i, row in df.iterrows():
        key = f"dsa_notes_edit_{row['#']}"
        val = st.text_input(f"Notes for #{row['#']} {row['Topic']}", value=row["Notes"], key=key)
        edited_notes.append(val)

    df["Notes"] = edited_notes

    def highlight_breaks(row):
        bg_color = '#D0E7FF' if row['Type'] == 'Break' else ''
        return ['background-color: {}'.format(bg_color)]*len(row)

    st.markdown("### DSA Schedule with Notes (Editable)")
    st.dataframe(df.style.apply(highlight_breaks, axis=1))

    if st.button("Save Notes"):
        for i, row in df.iterrows():
            for item in st.session_state.dsa_sheet:
                if ('#' in item and item['#'] == row['#']) or ('topic' in item and row['Topic'].startswith(item.get('topic',''))):
                    item['notes'] = row['Notes']
                    break
        save_data()
        st.success("Notes saved successfully!")
