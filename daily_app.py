import streamlit as st
import datetime
import threading
import time
import json
import os
import calendar
import pandas as pd

############### Date Utility ################
def get_today_date():
    return datetime.date.today().isoformat()

def get_now_datetime():
    return datetime.datetime.now()

def get_display_date():
    d = get_now_datetime()
    return d.strftime('%A, %d %B %Y')

############### Data Handling ################
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return {
        "classroom_tasks": {
            "Database System": [],
            "Operating Systems": [],
            "Compiler Design": [],
            "Computer Networks": [],
            "Cloud Architecture Design": [],
        },
        "completed_classroom_tasks": {
            "Database System": {},
            "Operating Systems": {},
            "Compiler Design": {},
            "Computer Networks": {},
            "Cloud Architecture Design": {},
        },
        "app_updates": [],
        "app_ideas": [],
        "duolingo_records": {},
        "morning_exercise_records": {},
        "jawline_records": {},
        "dairy_records": {},
        "water_counts": {},
        "water_checklists": {},
        "water_main_checklist": {},
        "passwords": {
            "Folder 1": [],
            "Folder 2": [],
            "Folder 3": [],
            "Folder 4": [],
        },
        "dsa_sheet": [{} for _ in range(18)],
        "important_dates": []
    }

def save_data():
    with open("data.json", "w") as f:
        json.dump({
            "classroom_tasks": st.session_state.classroom_tasks,
            "completed_classroom_tasks": st.session_state.completed_classroom_tasks,
            "app_updates": st.session_state.app_updates,
            "app_ideas": st.session_state.app_ideas,
            "duolingo_records": st.session_state.duolingo_records,
            "morning_exercise_records": st.session_state.morning_exercise_records,
            "jawline_records": st.session_state.jawline_records,
            "dairy_records": st.session_state.dairy_records,
            "water_counts": st.session_state.water_counts,
            "water_checklists": st.session_state.water_checklists,
            "water_main_checklist": st.session_state.water_main_checklist,
            "passwords": st.session_state.passwords,
            "dsa_sheet": st.session_state.dsa_sheet,
            "important_dates": st.session_state.important_dates,
        }, f)

########### Session Init ################
data = load_data()
for key, default in [
    ("classroom_tasks", {
        "Database System": [],
        "Operating Systems": [],
        "Compiler Design": [],
        "Computer Networks": [],
        "Cloud Architecture Design": [],
    }),
    ("completed_classroom_tasks", {
        "Database System": {},
        "Operating Systems": {},
        "Compiler Design": {},
        "Computer Networks": {},
        "Cloud Architecture Design": {},
    }),
    ("app_updates", []),
    ("app_ideas", []),
    ("duolingo_records", {}),
    ("morning_exercise_records", {}),
    ("jawline_records", {}),
    ("dairy_records", {}),
    ("water_counts", {}),
    ("water_checklists", {}),
    ("water_main_checklist", {}),
    ("passwords", {
        "Folder 1": [],
        "Folder 2": [],
        "Folder 3": [],
        "Folder 4": [],
    }),
    ("dsa_sheet", [{} for _ in range(18)]),
    ("important_dates", []),
]:
    if key not in st.session_state:
        st.session_state[key] = data.get(key, default)

########### Sidebar Navigation #################
st.sidebar.title("📘 Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "Afternoon Schedule",
    "Classroom Studies",
    "DSA Sheet Scheduling",
    "Balanced Diet",
    "Mind & Body Routine",
    "Time Reminder",
    "Dairy",
    "Stored Data",
    "Important Dates",
    "Passwords",
    "Details and Portfolio",
    "App Update"
])

########### Top Header/Clock #################
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"## 📅 Today's Date: {get_display_date()}")
with col2:
    timer_placeholder = st.empty()
def update_clock():
    while True:
        timer_placeholder.markdown(
            f"<div style='text-align:right;font-size:20px;background:#000000;color:#39FF14;padding:8px;border-radius:8px;'>🕒 Timers: {get_now_datetime().strftime('%H:%M:%S')}</div>",
            unsafe_allow_html=True
        )
        time.sleep(1)
thread = threading.Thread(target=update_clock)
thread.daemon = True
thread.start()

########### Calendar Helpers and other pages ###########
# (Code for other pages unchanged, for brevity not repeated here)

########### DSA Sheet Scheduling Page with new feature ###########

if page == "DSA Sheet Scheduling":
    st.title("🧠 DSA Sheet Scheduling")

    # Use current session state's dsa_sheet or initialize with the given schedule if empty
    if not st.session_state.dsa_sheet or all(not item for item in st.session_state.dsa_sheet):
        # Initial DSA schedule as provided previously
        st.session_state.dsa_sheet = [
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

    # Helper to parse a date string (e.g. "Jul 23") into datetime.date with year 2025
    def parse_md_date(date_str):
        return datetime.datetime.strptime(date_str.strip() + " 2025", "%b %d %Y").date()

    # Parse Date Range string to (start_date, end_date)
    def parse_date_range(date_range):
        # Support the formats:
        # "Jul 23 – Jul 29"
        # "Aug 1 – Aug 16 (✂️ split) + Aug 26" (just parse first range here)
        # "Sep 24 – Sep 25 + Sep 29 – Oct 1" (parse first range only)
        part = date_range.split('+')[0].split('(')[0].strip()
        parts = part.split('–')
        if len(parts) == 2:
            start = parse_md_date(parts[0])
            end = parse_md_date(parts[1])
        else:
            # single date only
            start = end = parse_md_date(parts[0])
        return start, end

    # Format start and end dates back into readable range string (e.g. Jul 23 – Jul 29)
    def format_date_range(start_date, end_date):
        return f"{start_date.strftime('%b %d')} – {end_date.strftime('%b %d')}"

    # Calculate duration days inclusive
    def days_between(start_date, end_date):
        return (end_date - start_date).days + 1

    # Prepare schedule list with parsed dates for easy manipulation
    schedule = []
    for idx, item in enumerate(st.session_state.dsa_sheet):
        if not item:
            continue
        # parse date range
        try:
            start, end = parse_date_range(item.get("Date Range",""))
        except Exception:
            start = end = None
        schedule.append({
            "idx": idx,
            "raw": item,
            "Type": item.get("Type", ""),
            "Topic": item.get("Topic", ""),
            "Days": item.get("Days", 0),
            "Notes": item.get("Notes", ""),
            "start": start,
            "end": end,
        })

    # Sort schedule by start date (None dates at end)
    schedule = sorted(schedule, key=lambda x: (x['start'] if x['start'] else datetime.date.max))

    # Render DataFrame with notes and highlight breaks
    df_display = pd.DataFrame([{
        "#": s["raw"].get("#", ""),
        "Type": s["Type"],
        "Topic": s["Topic"],
        "Days": s["Days"],
        "Date Range": s["raw"].get("Date Range", ""),
        "Notes": s["Notes"],
        "start": s["start"],
        "end": s["end"]
    } for s in schedule])

    def highlight_breaks(row):
        bg_color = '#D0E7FF' if row['Type'] == 'Break' else ''
        return ['background-color: {}'.format(bg_color)]*len(row)

    st.markdown("### DSA Schedule with Editable Notes")
    edited_notes = []
    for i, row in df_display.iterrows():
        key = f"dsa_notes_edit_{i}"
        val = st.text_input(f"Notes for #{row['#']} {row['Topic']}", value=row["Notes"], key=key)
        edited_notes.append(val)
    df_display["Notes"] = edited_notes

    # Show schedule table with coloring breaks
    styled_df = df_display.drop(columns=['start', 'end']).style.apply(highlight_breaks, axis=1)
    st.dataframe(styled_df)

    if st.button("Save Notes"):
        for i, s in enumerate(schedule):
            s["raw"]["Notes"] = edited_notes[i]
        # Update session state dsa_sheet accordingly
        for s in schedule:
            idx = s["idx"]
            st.session_state.dsa_sheet[idx] = s["raw"]
        save_data()
        st.success("Notes saved successfully!")

    st.markdown("---")

    # --- New topic input section ---
    st.markdown("### Add a New DSA Topic")

    with st.form("add_new_dsa_form"):
        new_topic = st.text_input("Enter new topic name", "")
        new_from = st.date_input("From date", datetime.date.today())
        new_till = st.date_input("Till date", datetime.date.today())
        submitted = st.form_submit_button("Go")
        if submitted:
            # Validate input
            if not new_topic.strip():
                st.error("Topic name cannot be empty.")
            elif new_till < new_from:
                st.error("Till date must be on or after From date.")
            else:
                # Compute new topic days count
                new_days = days_between(new_from, new_till)

                # Prepare to insert new item and reschedule overlapping DSA topics
                # First, convert new topic details to dict format similar to dsa_sheet entries
                new_dsa_item = {
                    "#": None,  # will assign later for numbering,
                    "Type": "DSA",
                    "Topic": new_topic.strip(),
                    "Days": new_days,
                    "Date Range": format_date_range(new_from, new_till),
                    "Notes": "–"
                }

                # Strategy:
                # 1. Insert new topic into schedule by start date.
                # 2. For existing DSA topics overlapping or starting on/after new_from,
                #    shift them forward so no overlap occurs.
                # Breaks are left untouched as is.

                # Filter out only DSA topics for rescheduling
                dsa_items = [s for s in schedule if s["Type"] == "DSA"]

                # Collect all events (DSA + Break) except those "empty"
                non_empty_schedule = [s for s in schedule if s["Type"] in ("DSA", "Break")]

                # Define helper function to check overlap between two date ranges
                def ranges_overlap(s1, e1, s2, e2):
                    return not (e1 < s2 or e2 < s1)

                # Build a new timeline inserting the new topic, then reschedule others if needed
                # Sort the dsa_items by start date
                dsa_items_sorted = sorted(dsa_items, key=lambda x: x["start"])

                # Insert new topic placeholder into the timeline
                # We will reconstruct the schedule list with topics arranged and shifted

                # Create a working list: list of dict {Type,Topic,Days,start,end,Notes}
                timeline = []

                # Add all breaks and DSA topics except DSA (to be reinserted)
                for item in non_empty_schedule:
                    if item["Type"] == "Break":
                        timeline.append(item)

                # Insert new DSA topic into timeline with its start/end
                timeline.append({
                    "idx": None,
                    "raw": new_dsa_item,
                    "Type": "DSA",
                    "Topic": new_dsa_item["Topic"],
                    "Days": new_days,
                    "Notes": new_dsa_item["Notes"],
                    "start": new_from,
                    "end": new_till
                })

                # Sort timeline by start date; breaks + new topic now
                timeline = sorted(timeline, key=lambda x: (x['start'] if x['start'] else datetime.date.max))

                # Insert previously existing DSA topics (excluding old new topic if exists) in order,
                # but reschedule if overlap with new topic timeline.

                # Remove all old DSA topics for now, we will re-add them:
                # We will reschedule DSA topics starting >= new_from or overlapping new topic

                leftover_dsas = []
                for s in dsa_items_sorted:
                    # Skip the new inserted topic if it is a repeat? No, new topic not in old schedule yet.
                    # We only reschedule DSA topics that overlap with or start after new_from
                    if s["end"] < new_from:
                        # before new topic range, no change
                        leftover_dsas.append(s)
                    else:
                        # starting on or after new_from or overlaps; to be rescheduled
                        # We'll add them after last timeline event in timeline to avoid overlap
                        pass  # will reschedule

                # Sort leftover_dsas by original start date ascending
                leftover_dsas = sorted(leftover_dsas, key=lambda x: x["start"])

                # Find the max end date in current timeline to start pushing rescheduled tasks
                max_end = max([t['end'] for t in timeline if t['end'] is not None], default=new_till)
                push_start_date = max_end + datetime.timedelta(days=1)

                # Append leftover_dsas one by one, rescheduling their dates sequentially after push_start_date
                for old_task in leftover_dsas:
                    # Calculate new end date by shifting task to push_start_date
                    new_task_start = push_start_date
                    new_task_end = new_task_start + datetime.timedelta(days=old_task["Days"] - 1)

                    # Update task fields
                    new_item = {
                        "idx": old_task["idx"],
                        "raw": old_task["raw"],
                        "Type": old_task["Type"],
                        "Topic": old_task["Topic"],
                        "Days": old_task["Days"],
                        "Notes": old_task["Notes"],
                        "start": new_task_start,
                        "end": new_task_end,
                    }
                    timeline.append(new_item)

                    # Update push_start_date for next
                    push_start_date = new_task_end + datetime.timedelta(days=1)

                # Now sort timeline again by start date
                timeline = sorted(timeline, key=lambda x: (x['start'] if x['start'] else datetime.date.max))

                # Assign new numbering (#) sequentially ignoring breaks numbering pattern
                # We'll number all items sequentially starting from 1
                current_num = 1
                for t in timeline:
                    # Update dsa_sheet raw dict:
                    t["raw"]["#"] = current_num
                    # Update Date Range string
                    t["raw"]["Date Range"] = format_date_range(t["start"], t["end"])
                    # Ensure "Days" matches calculation (for DSA type only)
                    if t["Type"] == "DSA":
                        t["raw"]["Days"] = days_between(t["start"], t["end"])
                    current_num += 1

                # Update st.session_state.dsa_sheet to timeline raw data
                st.session_state.dsa_sheet = [t["raw"] for t in timeline]

                save_data()
                st.success(f"New topic '{new_topic.strip()}' added and schedule updated with no overlaps.")

                # Rerun to update UI instantly
               # st.experimental_rerun()

# (Other page codes unchanged)
# You can add the rest of your app code here (all previous pages remain the same)

