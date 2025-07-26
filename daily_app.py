import streamlit as st
import pandas as pd
import datetime
import uuid
import copy

st.set_page_config(page_title="DSA Daily Scheduler", layout="wide")

def date_fmt(dt):
    if isinstance(dt, pd.Timestamp):
        dt = dt.date()
    return dt.strftime('%d/%m/%y')

def daterange_fmt(start, end):
    if isinstance(start, pd.Timestamp):
        start = start.date()
    if isinstance(end, pd.Timestamp):
        end = end.date()
    if start == end:
        return date_fmt(start)
    return f"{date_fmt(start)} – {date_fmt(end)}"

def parse_date(s):
    try:
        return datetime.datetime.strptime(s, "%d/%m/%y").date()
    except Exception:
        return None

def overlaps(a_start, a_end, b_start, b_end):
    if any(v is None for v in [a_start,a_end,b_start,b_end]):
        return False
    return a_start <= b_end and b_start <= a_end

def get_uid():
    return str(uuid.uuid4())

def next_day(d):
    if isinstance(d, pd.Timestamp):
        d = d.date()
    return d + datetime.timedelta(days=1)

def days_between(start, end):
    if isinstance(start, pd.Timestamp):
        start = start.date()
    if isinstance(end, pd.Timestamp):
        end = end.date()
    return (end - start).days + 1

def subtract_intervals(interval, blockers):
    """
    Given interval (start,end) and a list of blocker intervals [(s,e),...],
    return list of intervals representing parts of interval excluding blockers.
    Assumes blocker intervals do not overlap and are sorted.
    """
    start, end = interval
    result = []
    current_start = start

    for b_start, b_end in blockers:
        if b_end < current_start:
            continue
        if b_start > end:
            break
        # If blocker starts before current_start, move to blocker end+1
        if b_start <= current_start <= b_end:
            current_start = next_day(b_end)
            continue
        # blocker after current_start but before end
        if current_start < b_start:
            block_interval_end = prev_day(b_start)
            if block_interval_end >= current_start:
                result.append((current_start, min(block_interval_end, end)))
            current_start = next_day(b_end)
    if current_start <= end:
        result.append((current_start, end))
    return result

# DEFAULT DATA initialization (same as before)
DEFAULT_DATA = [
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
    st.session_state.dsa_sheet = copy.deepcopy(DEFAULT_DATA)

def _save_data():
    # Persistence placeholder
    pass

def expand_all_ranges(rows):
    out = []
    for row in rows:
        drs = row["Date Range"].split(",")
        for dr in drs:
            dr = dr.strip()
            if "–" in dr:
                parts = dr.split("–")
                start = parse_date(parts[0].strip())
                end = parse_date(parts[1].strip())
            else:
                start = end = parse_date(dr)
            if start is not None and end is not None:
                out.append((row, start, end))
    return out

def split_topic_by_breaks(topic_interval, breaks_sorted):
    """Given (start,end) of topic and sorted list of break intervals,
    return list of (start,end) segments of topic split only at breaks."""
    topic_start, topic_end = topic_interval
    # Collect break intervals overlapping or between topic start-end
    blocking_intervals = []
    for b_start, b_end in breaks_sorted:
        # Only consider breaks that overlap or are within topic interval
        if not (b_end < topic_start or b_start > topic_end):
            # Clip break to topic bounds
            blocking_intervals.append((
                max(topic_start, b_start),
                min(topic_end, b_end)
            ))
    # Sort and merge overlapping/adjacent blocks:
    if not blocking_intervals:
        return [(topic_start, topic_end)]

    blocking_intervals.sort()
    merged_blocks = []
    current_s, current_e = blocking_intervals[0]

    for s, e in blocking_intervals[1:]:
        if s <= current_e + datetime.timedelta(days=1):
            current_e = max(current_e, e)
        else:
            merged_blocks.append((current_s, current_e))
            current_s, current_e = s, e
    merged_blocks.append((current_s, current_e))

    # Now subtract blocking intervals from topic interval
    result_segments = []
    current_pos = topic_start
    for b_s, b_e in merged_blocks:
        if current_pos < b_s:
            # Append segment before break
            result_segments.append((current_pos, b_s - datetime.timedelta(days=1)))
        current_pos = b_e + datetime.timedelta(days=1)
    if current_pos <= topic_end:
        result_segments.append((current_pos, topic_end))
    return result_segments

def reschedule_dsa(entries, new_topic=None, delete_uid=None):
    """
    Reschedules DSA topics with splitting only at Break boundaries.
    Keeps Breaks locked.
    """
    events = copy.deepcopy(entries)
    if delete_uid:
        events = [e for e in events if e['UID'] != delete_uid]

    breaks = [e for e in events if e["Type"] == "Break"]
    dsa = [e for e in events if e["Type"] == "DSA"]

    # Parse all breaks into intervals, sorted
    break_intervals = []
    for b in breaks:
        for _, s, e in expand_all_ranges([b]):
            break_intervals.append((s,e))
    break_intervals.sort()

    # If new topic added, insert it as locked break-equivalent (fixed)
    new_topic_intervals = []
    if new_topic:
        new_start = new_topic['start']
        new_end = new_topic['end']
        new_topic_intervals.append((
            new_start, new_end, {
                "Type": "DSA",
                "Topic": new_topic['topic'],
                "Notes": new_topic.get("note", ""),
                "UID": get_uid()
            }
        ))

    # Build combined timeline of breaks + new_topic to lock dates
    locked_intervals = [*[(s,e,b) for b,s,e in [(b,) + bi for bi in break_intervals]]]
    for ni in new_topic_intervals:
        locked_intervals.append(ni)
    # Sort locked intervals by start date (ignoring the objects for sorting)
    locked_intervals.sort(key=lambda x: x[0])

    # Scheduled result events list
    scheduled = []

    # Helper: find next free date after given date (not in locked)
    def next_free_date_from(date, after_locked):
        d = date
        locked_starts = [li[0] for li in after_locked]
        locked_ends = [li[1] for li in after_locked]
        while True:
            # Check if d in any locked interval
            in_locked = False
            for s,e,_ in after_locked:
                if s <= d <= e:
                    in_locked = True
                    d = e + datetime.timedelta(days=1)
                    break
            if not in_locked:
                return d

    # Start from earliest min date of schedule or today
    all_dates = []
    for row, s, e in expand_all_ranges(events):
        all_dates.append(s)
    base_date = min(all_dates) if all_dates else datetime.date.today()

    # Position pointer for scheduling
    cursor = base_date

    # To number splits like 1, 1.1, 1.2 for split topics
    topic_splits_count = {}

    # List topics in order of their earliest start date (combine multi-ranges if needed by earliest)
    def earliest_start(r):
        drs = r["Date Range"].split(",")
        starts = [parse_date(d.split("–")[0].strip()) for d in drs]
        return min(starts)

    dsa_sorted = sorted(dsa, key=earliest_start)
    # Insert new topic into dsa_sorted at correct place (remove any duplicates if same topic)

    if new_topic:
        # Remove any existing topics identical by name? No, keep all
        pass

    # Build a "new" schedule with locked breaks and new topic as fixed
    # We'll assign new dates to DSA topics, split only at breaks

    def get_blocks():
        # return list of locked intervals + new topic intervals as (start,end,obj)
        blocks = []
        for s,e,b in locked_intervals:
            blocks.append((s,e,b))
        return blocks

    blocks = get_blocks()

    # Sort blocks by start date
    blocks.sort(key=lambda x: x[0])

    # We'll keep track of the locked intervals as a set of dates for quick lookup
    locked_dates = set()
    for s,e,_ in blocks:
        current = s
        while current <= e:
            locked_dates.add(current)
            current = current + datetime.timedelta(days=1)

    # After placing breaks & new topic locked, schedule each DSA topic

    for topic in dsa_sorted:
        # If this is the new_topic (by Topic name), schedule it at user requested dates
        if new_topic and topic["Topic"] == new_topic['topic']:
            # use new_topic start/end as interval
            segs = [(new_topic['start'], new_topic['end'])]
        else:
            # Get all original date ranges for this topic (can be multiple)
            segs_orig = []
            for _,s,e in expand_all_ranges([topic]):
                segs_orig.append((s,e))

            segs = []
            # For each original range, split by breaks only
            for seg in segs_orig:
                splits = split_topic_by_breaks(seg, break_intervals)
                segs.extend(splits)

        # For each segment scheduled, assign dates respecting locked intervals and cursor,
        # actually we follow original segment dates (because breaks fixed)
        # But if the new_topic overlaps, stretch other topics after it.

        for idx_seg, (seg_start, seg_end) in enumerate(segs):
            # Find number for split (1-based index) per topic
            key = topic['Topic']
            topic_splits_count[key] = topic_splits_count.get(key, 0) + 1
            split_num = topic_splits_count[key]

            # Format topic name with split only if >1 segment
            if len(segs) > 1:
                display_topic = f"{topic['Topic']} (part {split_num})"
            else:
                display_topic = topic['Topic']

            days = days_between(seg_start, seg_end)

            # Add scheduled entry
            scheduled.append({
                "S No.": 0,
                "Type": "DSA",
                "Topic": display_topic,
                "Days": days,
                "Date Range": daterange_fmt(seg_start, seg_end),
                "Notes": topic.get("Notes", ""),
                "UID": topic.get("UID", get_uid())
            })

    # Add breaks separately at their fixed positions
    # Breaks already have date ranges, add them as is
    for b in breaks:
        # for multi date ranges, keep as separate rows (if needed)
        drs = b["Date Range"].split(",")
        for dr in drs:
            dr = dr.strip()
            if "–" in dr:
                start = parse_date(dr.split("–")[0].strip())
                end = parse_date(dr.split("–")[1].strip())
            else:
                start = end = parse_date(dr)
            days = days_between(start, end)
            scheduled.append({
                "S No.": 0,
                "Type": "Break",
                "Topic": b["Topic"],
                "Days": days,
                "Date Range": daterange_fmt(start, end),
                "Notes": b.get("Notes", ""),
                "UID": b.get("UID", get_uid())
            })

    # Add any new_topic breaks for safety if new_topic is Break (rare)
    if new_topic and new_topic.get('type',"DSA") == "Break":
        start = new_topic['start']
        end = new_topic['end']
        days = days_between(start,end)
        scheduled.append({
            "S No.": 0,
            "Type": "Break",
            "Topic": new_topic['topic'],
            "Days": days,
            "Date Range": daterange_fmt(start,end),
            "Notes": new_topic.get("note",""),
            "UID": get_uid()
        })

    # Sort all scheduled by start date
    def start_date(ev):
        return parse_date(ev["Date Range"].split("–")[0].strip())

    scheduled.sort(key=start_date)

    # Now resolve date overlaps with inserted new topic:
    # We push DSA topics after new topic if overlapping
    if new_topic:
        new_s = new_topic['start']
        new_e = new_topic['end']
        pushed_dates = []

        # Since breaks fixed, only shift DSA topics starting after new_s if overlap

        for ev in scheduled:
            if ev["Type"] == "DSA":
                ev_start = parse_date(ev["Date Range"].split("–")[0].strip())
                ev_end = parse_date(ev["Date Range"].split("–")[-1].strip())

                # Overlap condition
                if ev_start <= new_e and ev_end >= new_s:
                    # Need to push this event to after new_e
                    push_by = (new_e - ev_start) + datetime.timedelta(days=1)
                    new_start = new_e + datetime.timedelta(days=1)

                    # Calculate days count same as before
                    days = ev["Days"]

                    ev["Date Range"] = daterange_fmt(new_start, new_start + datetime.timedelta(days=days-1))
                    # Note: This simplified logic pushes overlapping events forward to start the day after new topic ends

    # Re-number
    for idx, ev in enumerate(scheduled, 1):
        ev["S No."] = idx

    return scheduled

def main():
    st.title("📅 DSA Sheet Scheduler (Daily App)")

    st.info(
        "Add study topics, breaks, or fun/wasted events below! Schedule splits topics only at breaks. Breaks stay fixed. Delete or add rows as needed."
    )

    # Reschedule at start to have fresh dates & splits
    st.session_state.dsa_sheet = reschedule_dsa(st.session_state.dsa_sheet)
    df = pd.DataFrame(st.session_state.dsa_sheet)

    if not df.empty:
        st.subheader("DSA Schedule Table")

        show_df = df.drop(columns=["UID"])
        st.dataframe(show_df, use_container_width=True)

        st.markdown("### Delete any row:")
        for i, row in df.iterrows():
            col1, col2 = st.columns([8, 2])
            s_no = row['S No.'] if 'S No.' in row else i + 1
            col1.markdown(f"**{s_no}. {row['Type']} — {row['Topic']}** ({row['Date Range']})")
            delete_clicked = col2.button(f"🗑️ Delete", key=f"del_{row['UID']}")
            if delete_clicked:
                st.session_state.dsa_sheet = reschedule_dsa(
                    st.session_state.dsa_sheet,
                    delete_uid=row['UID']
                )
                _save_data()
                st.experimental_rerun()
    else:
        st.info("No schedule entries found yet.")

    today = datetime.date.today()
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Add Entries")

    with st.form("add_study"):
        st.markdown("<div style='background:#e9ffe9;padding:10px;border-radius:6px;'><b>🟩 Add Study</b></div>", unsafe_allow_html=True)
        study_topic = st.text_input("Study Topic (e.g. Trees)", key="study_topic_input")
        study_from = st.date_input("From Date", key="study_from_input", value=today)
        study_to = st.date_input("Till Date", key="study_to_input", value=today)
        study_note = st.text_input("Notes (optional)", key="study_note_input", value="✅ Manually Added")
        go1 = st.form_submit_button("➕ Add Study")

    with st.form("add_fun"):
        st.markdown("<div style='background:#ffeaea;padding:10px;border-radius:6px;'><b>🟥 Add Fun Activity / Break</b></div>", unsafe_allow_html=True)
        fun_topic = st.text_input("Fun Topic (e.g. Movie)", key="fun_topic_input")
        fun_from = st.date_input("From (Break)", key="fun_from_input", value=today)
        fun_to = st.date_input("Till (Break)", key="fun_to_input", value=today)
        fun_note = st.text_input("Fun Notes (optional)", key="fun_note_input", value="🎈 Fun/Enjoyment")
        go2 = st.form_submit_button("➕ Add Fun")

    with st.form("add_waste"):
        st.markdown("<div style='background:#efefef;padding:10px;border-radius:6px;'><b>⬜ Add Wasted Time</b></div>", unsafe_allow_html=True)
        waste_reason = st.text_input("Wasted Reason", key="waste_reason_input")
        waste_from = st.date_input("From (Wasted)", key="waste_from_input", value=today)
        waste_to = st.date_input("Till (Wasted)", key="waste_to_input", value=today)
        waste_note = st.text_input("Waste Notes (optional)", key="waste_note_input", value="😓 Time Wasted")
        go3 = st.form_submit_button("➕ Add Wasted")

    if go1:
        if not study_topic.strip():
            st.error("Please enter a study topic.")
        elif study_from > study_to:
            st.error("From date cannot be after Till date.")
        else:
            new_entry = {
                'topic': study_topic.strip(),
                'start': study_from,
                'end': study_to,
                'note': study_note.strip(),
                'type': 'DSA'
            }
            st.session_state.dsa_sheet = reschedule_dsa(st.session_state.dsa_sheet, new_topic=new_entry)
            _save_data()
            st.success("Added Study topic and rescheduled!")
            st.experimental_rerun()

    if go2:
        if not fun_topic.strip():
            st.error("Please enter a fun topic.")
        elif fun_from > fun_to:
            st.error("From date cannot be after Till date.")
        else:
            new_break = {
                "Type": "Break",
                "Topic": fun_topic.strip(),
                "Days": (fun_to - fun_from).days + 1,
                "Date Range": daterange_fmt(fun_from, fun_to),
                "Notes": fun_note.strip(),
                "UID": get_uid()
            }
            st.session_state.dsa_sheet.append(new_break)
            # No new topic insertion, just reschedule to maintain order
            st.session_state.dsa_sheet = reschedule_dsa(st.session_state.dsa_sheet)
            _save_data()
            st.success("Added new Break/Fun activity!")
            st.experimental_rerun()

    if go3:
        if not waste_reason.strip():
            st.error("Please enter a wasted time reason.")
        elif waste_from > waste_to:
            st.error("From date cannot be after Till date.")
        else:
            new_break = {
                "Type": "Break",
                "Topic": waste_reason.strip(),
                "Days": (waste_to - waste_from).days + 1,
                "Date Range": daterange_fmt(waste_from, waste_to),
                "Notes": waste_note.strip(),
                "UID": get_uid()
            }
            st.session_state.dsa_sheet.append(new_break)
            st.session_state.dsa_sheet = reschedule_dsa(st.session_state.dsa_sheet)
            _save_data()
            st.success("Logged wasted time as Break!")
            st.experimental_rerun()

    st.markdown("---")
    st.markdown("Made with ❤️ for efficient DSA prep! [Perplexity AI App Example]")

if __name__ == "__main__":
    main()
