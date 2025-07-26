import streamlit as st
import pandas as pd
import datetime
import uuid

st.set_page_config(page_title="DSA Daily Scheduler", layout="wide")

####### ---------- HELPER FUNCTIONS ------------- #######

def date_fmt(dt):
    return dt.strftime('%d/%m/%y')

def daterange_fmt(start, end):
    if start == end:
        return date_fmt(start)
    return f"{date_fmt(start)} – {date_fmt(end)}"

def parse_date(s):
    try:
        return datetime.datetime.strptime(s, "%d/%m/%y").date()
    except Exception:
        return None

def overlaps(a_start, a_end, b_start, b_end):
    return a_start <= b_end and b_start <= a_end

def get_uid():
    return str(uuid.uuid4())

def next_day(d):
    return d + datetime.timedelta(days=1)

def prev_day(d):
    return d - datetime.timedelta(days=1)

###### --------- DATA AND INITIALIZATION ---------- ######

DEFAULT_DATA = [
    # S.No, Type, Topic, Days, Date Range, Notes, UID
    {"Type": "DSA", "Topic": "LinkedList", "Days": 9, "Date Range": "27/07/25 – 04/08/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Recursion", "Days": 6, "Date Range": "05/08/25 – 10/08/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Bit Manipulation (Part 1)", "Days": 3, "Date Range": "11/08/25 – 13/08/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "CAT-1", "Days": 12, "Date Range": "14/08/25 – 25/08/25", "Notes": "🧠 Exams", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Bit Manipulation (Part 2)", "Days": 2, "Date Range": "26/08/25 – 27/08/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Stack & Queues", "Days": 7, "Date Range": "28/08/25 – 03/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Sliding Window", "Days": 6, "Date Range": "04/09/25 – 09/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Heaps", "Days": 5, "Date Range": "10/09/25 – 14/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Greedy Algorithms", "Days": 7, "Date Range": "15/09/25 – 24/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "Gravitas", "Days": 5, "Date Range": "25/09/25 – 29/09/25", "Notes": "🎓 Event", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Binary Trees (Part 1)", "Days": 2, "Date Range": "30/09/25 – 01/10/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "CAT-2", "Days": 12, "Date Range": "02/10/25 – 13/10/25", "Notes": "🧠 Exams", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Binary Trees (Part 2)", "Days": 10, "Date Range": "14/10/25 – 16/10/25, 19/10/25 – 25/10/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "Diwali Travel 1", "Days": 2, "Date Range": "17/10/25 – 18/10/25", "Notes": "🪔 Festival", "UID": get_uid()},
    {"Type": "Break", "Topic": "Diwali Travel 2", "Days": 2, "Date Range": "26/10/25 – 27/10/25", "Notes": "🛫 Travel", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Binary Search Trees", "Days": 3, "Date Range": "28/10/25 – 30/10/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Graphs (Part 1)", "Days": 5, "Date Range": "31/10/25 – 05/11/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "FAT & Labs + FAT", "Days": 31, "Date Range": "06/11/25 – 06/12/25", "Notes": "📚 Exams", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Graphs (Part 2)", "Days": 9, "Date Range": "07/12/25 – 15/12/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Dynamic Programming", "Days": 16, "Date Range": "16/12/25 – 31/12/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Tries", "Days": 5, "Date Range": "01/01/26 – 05/01/26", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Strings", "Days": 7, "Date Range": "06/01/26 – 12/01/26", "Notes": "", "UID": get_uid()},
]

if "dsa_sheet" not in st.session_state:
    st.session_state.dsa_sheet = DEFAULT_DATA.copy()

def _save_data():
    # For real app you could pickle/csv/save, but in-memory for now
    pass

###### ---------- ADVANCED RESCHEDULING CORE ---------- ######


def expand_all_ranges(rows):
    """Expand all date ranges into list of (row, start, end)"""
    out = []
    for row in rows:
        drs = row["Date Range"].split(",")
        for dr in drs:
            if "–" in dr:
                parts = dr.strip().split("–")
                start = parse_date(parts[0].strip())
                end = parse_date(parts[1].strip())
            else:
                d = parse_date(dr.strip())
                start, end = d, d
            out.append((row, start, end))
    return out

def reschedule_dsa_with_interruptions(entries, new_topic=None, delete_uid=None):
    """Given current schedule, plus a possible new DSA insertion, and optionally a row to delete,
    returns a new schedule with correct splits and assigned dates."""

    # Step 1: Filter and process
    events = [dict(row) for row in entries]  # deep copy!
    # Optionally remove deleted row
    if delete_uid:
        events = [e for e in events if e['UID'] != delete_uid]

    # Step 2: Separate out all breaks and DSA
    breaks = [e for e in events if e["Type"] == "Break"]
    dsa = [e for e in events if e["Type"] == "DSA"]
    # Today becomes minimum start date
    all_dates = []
    for r, s, e in expand_all_ranges(events):
        all_dates.append(s)
    base_date = min(all_dates) if all_dates else datetime.date.today()

    # Step 3: Build a list of locked intervals (breaks)
    locked = []
    for b in breaks:
        for _, s, e in expand_all_ranges([b]):
            locked.append( (s, e, b) )

    # Step 4: Prepare interruptions/new
    interruptions = []
    if new_topic:
        interruptions.append( (new_topic['start'], new_topic['end'], {
            "Type": "DSA", "Topic": new_topic['topic'],
            "Days": (new_topic['end']-new_topic['start']).days+1,
            "Date Range": daterange_fmt(new_topic['start'], new_topic['end']),
            "Notes": new_topic.get("note", ""),
            "UID": get_uid()
        }) )

    # Step 5: Timeline assignment, day by day...
    all_dsa_topics = []
    for dsa_i, d in enumerate(dsa):
        for _, start, end in expand_all_ranges([d]):
            all_dsa_topics.append({
                'orig_topic': d['Topic'],
                'orig_uid': d['UID'],
                'notes': d.get("Notes",""),
                'length': (end-start).days+1,
            })

    flat_dsa_seq = []
    for seg in all_dsa_topics:
        flat_dsa_seq.extend([{
            "Topic": seg["orig_topic"],
            "UID": seg["orig_uid"],
            "Notes": seg.get("notes","")
        }] * seg["length"])

    # Step 6: Go day by day, filling calendar
    # Build set of protected periods (breaks, interruptions)
    protected_cells = []
    for s,e,b in locked + interruptions:
        d0 = s
        while d0 <= e:
            protected_cells.append( (d0, b if isinstance(b, dict) else b ) )
            d0 = next_day(d0)

    # Build chrono list
    output = []
    pointer = base_date
    dsa_counter = 0
    numbering = dict()
    sub_number = dict()
    dsa_topic_tracker = {}
    # Get a list of all occupied days to jump gaps (skip breaks)
    reserved = {d for d, _ in protected_cells}
    # merge interruptions into calendar

    # Now, repeatedly pick up the DSA queue, slot to unoccupied dates
    while dsa_counter < len(flat_dsa_seq):
        # If pointer in reserved, find the protected (break/interruption) and append
        found = False
        for d, b in protected_cells:
            if d == pointer:
                # Only insert once per block (per start)
                if not output or output[-1].get('UID') != b.get("UID"):
                    event = dict(b)
                    event['Days'] = 1
                    event['Date Range'] = daterange_fmt(pointer, pointer)
                    if 'Type' not in event: event['Type'] = "Break"
                    event.setdefault("UID", get_uid())
                    output.append(event)
                else:
                    # Extend date range if subsequent day
                    output[-1]['Days'] += 1
                    p_start = parse_date(output[-1]["Date Range"].split("–")[0].strip())
                    output[-1]["Date Range"] = daterange_fmt(p_start, pointer)
                found = True
                break
        if found:
            pointer = next_day(pointer)
            continue
        # Otherwise, add a DSA topic chunk
        topic = flat_dsa_seq[dsa_counter]
        tname = topic['Topic']
        dsa_topic_tracker.setdefault(tname, 0)
        dsa_topic_tracker[tname] += 1
        dsa_cnum = dsa_topic_tracker[tname]
        # Sub-number for splitting
        if dsa_cnum == 1:
            show_name = tname
        else:
            show_name = f"{tname} (continued {dsa_cnum})"
        rec = {
            "Type": "DSA",
            "Topic": show_name,
            "Days": 1,
            "Date Range": daterange_fmt(pointer, pointer),
            "Notes": topic.get('Notes',""),
            "UID": get_uid()
        }
        # If previous output is same topic part, merge days
        if output and output[-1]["Topic"] == show_name:
            output[-1]["Days"] += 1
            parts = output[-1]["Date Range"].split("–")
            pstart = parse_date(parts[0].strip())
            output[-1]["Date Range"] = daterange_fmt(pstart, pointer)
        else:
            output.append(rec)
        dsa_counter += 1
        pointer = next_day(pointer)
    # Step 7: Insert interruptions and breaks again with preserved UIDs (avoid duplicate blocks)
    for s, e, b in interruptions+locked:
        # Fill with correct Days/range (already set)
        inserted = False
        for idx, row in enumerate(output):
            if row.get("UID") == b.get("UID"):
                inserted = True
        if not inserted:  # In rare cases where break is not in loop above
            br = dict(b)
            br['Date Range'] = daterange_fmt(s, e)
            br['Days'] = (e-s).days+1
            output.append(br)
    # Step 8: Sort by earliest date
    def row_start(row):
        start = parse_date(row["Date Range"].split("–")[0].strip())
        return start
    output = sorted(output, key=row_start)
    # Re-number
    for n, row in enumerate(output,1):
        row["S No."] = n
    return output

###### ----------- MAIN APP UI & LOGIC ----------- #######

def main():
    st.title("📅 DSA Sheet Scheduler (Daily App)")

    st.info("Add study topics, breaks, or fun/wasted events below! Your DSA schedule will split/reschedule automatically to avoid date overlaps. Breaks stay fixed. You can delete any row. 'Save Notes' will store notes for each row.")

    # --- Show Current Table (with DELETE per row) ---
    df = pd.DataFrame(st.session_state.dsa_sheet)
    if not df.empty:
        st.subheader("DSA Schedule Table")
        del_button_cols = st.columns(len(df)+1)  # All rows, for delete

        # Manual table with delete buttons
        table_data = []
        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            # Gather
            table_data.append([
                row_dict.get("S No.", idx+1),
                row_dict["Type"],
                row_dict["Topic"],
                row_dict["Days"],
                row_dict["Date Range"],
                row_dict.get("Notes", ""),
                row_dict["UID"]
            ])

        table_df = pd.DataFrame(table_data, columns=["S No.", "Type", "Topic", "Days", "Date Range", "Notes", "UID"])
        # Display table
        st.dataframe(table_df.drop(columns=["UID"]), use_container_width=True)

        # Per-row delete
        for i, row in table_df.iterrows():
            col1, _, col2 = st.columns([5,1,1])
            col1.markdown(f"**{row['S No.']}. {row['Type']} — {row['Topic']}** ({row['Date Range']})")
            if col2.button(f"🗑️ Delete row {row['S No.']}", key=f"delrowbtn_{row['UID']}"):
                # Remove and reschedule!
                st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(
                    st.session_state.dsa_sheet,
                    new_topic=None,
                    delete_uid=row['UID']
                )
                _save_data()
                st.experimental_rerun()

    else:
        st.info("No DSA entries yet.")

    # ------ Add Study / Fun / Wasted (INPUT BARS) ------
    today = datetime.date.today()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Add Entries")
    # Green: Study (DSA)
    with st.form("add_study"):
        st.markdown("<div style='background:#e9ffe9;padding:10px;border-radius:6px;'><b>🟩 Add Study</b></div>", unsafe_allow_html=True)
        topic = st.text_input("Study Topic (e.g. Trees)", key="study_topic_bar")
        from_date = st.date_input("From Date", key="study_from", value=today)
        to_date = st.date_input("Till Date", key="study_to", value=today)
        note = st.text_input("Notes", key="study_note", value="✅ Manually Added")
        go1 = st.form_submit_button("➕ Add Study")

    # Red: Fun/Break
    with st.form("add_fun"):
        st.markdown("<div style='background:#ffeaea;padding:10px;border-radius:6px;'><b>🟥 Add Fun Activity / Break</b></div>", unsafe_allow_html=True)
        fun_topic = st.text_input("Fun Topic (e.g. Movie)", key="fun_topic")
        fun_from = st.date_input("From (Break)", key="fun_from", value=today)
        fun_to = st.date_input("Till (Break)", key="fun_to", value=today)
        fun_note = st.text_input("Fun Notes", key="fun_note", value="🎈 Fun/Enjoyment")
        go2 = st.form_submit_button("➕ Add Fun")

    # Gray: Wasted
    with st.form("add_waste"):
        st.markdown("<div style='background:#efefef;padding:10px;border-radius:6px;'><b>⬜ Add Wasted Time</b></div>", unsafe_allow_html=True)
        waste_reason = st.text_input("Wasted Reason", key="waste_reason")
        waste_from = st.date_input("From (Wasted)", key="waste_from", value=today)
        waste_to = st.date_input("Till (Wasted)", key="waste_to", value=today)
        waste_note = st.text_input("Waste Notes", key="waste_note", value="😓 Time Wasted")
        go3 = st.form_submit_button("➕ Add Wasted")

    # Logic for Add buttons
    if go1:
        if not topic or from_date > to_date:
            st.error("Please enter valid topic/dates.")
        else:
            # Add study as DSA with split/reschedule
            st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(
                st.session_state.dsa_sheet,
                new_topic=dict(topic=topic, start=from_date, end=to_date, note=note)
            )
            _save_data()
            st.success("Added Study topic and rescheduled!")
            st.experimental_rerun()

    if go2:
        if not fun_topic or fun_from > fun_to:
            st.error("Enter proper fun topic and date range.")
        else:
            # Treat as Break, append as hard break and reschedule (breaks are fixed)
            new_break = {
                "Type": "Break",
                "Topic": fun_topic,
                "Days": (fun_to-fun_from).days+1,
                "Date Range": daterange_fmt(fun_from, fun_to),
                "Notes": fun_note,
                "UID": get_uid()
            }
            st.session_state.dsa_sheet.append(new_break)
            # Now reschedule (so this break locks its period)
            st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(st.session_state.dsa_sheet)
            _save_data()
            st.success("Added new Break/fun!")
            st.experimental_rerun()

    if go3:
        if not waste_reason or waste_from > waste_to:
            st.error("Enter proper reason/dates.")
        else:
            new_break = {
                "Type": "Break",
                "Topic": waste_reason,
                "Days": (waste_to - waste_from).days+1,
                "Date Range": daterange_fmt(waste_from, waste_to),
                "Notes": waste_note,
                "UID": get_uid()
            }
            st.session_state.dsa_sheet.append(new_break)
            st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(st.session_state.dsa_sheet)
            _save_data()
            st.success("Wasted time entry logged as Break.")
            st.experimental_rerun()

    # ------- Save Notes (for each row) -------
    if df.shape[0] > 0:
        if st.button("💾 Save Notes"):
            updated = []
            for idx, row in df.iterrows():
                uid = row["UID"]
                # In real world, probably also allow editing!
                updated.append({**row, "Notes": row.get("Notes", "")})
            st.session_state.dsa_sheet = updated
            _save_data()
            st.success("Notes saved.")

    st.markdown("---")
    st.markdown("Made with ❤️ for efficient DSA prep! [Perplexity AI App Example]")

if __name__ == "__main__":
    main()
