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

def prev_day(d):
    if isinstance(d, pd.Timestamp):
        d = d.date()
    return d - datetime.timedelta(days=1)

def days_between(start, end):
    if isinstance(start, pd.Timestamp):
        start = start.date()
    if isinstance(end, pd.Timestamp):
        end = end.date()
    return (end - start).days + 1

def split_topic_by_breaks(topic_interval, breaks_sorted):
    topic_start, topic_end = topic_interval
    blocking_intervals = []
    for b_start, b_end in breaks_sorted:
        if not (b_end < topic_start or b_start > topic_end):
            blocking_intervals.append((
                max(topic_start, b_start),
                min(topic_end, b_end)
            ))
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

    result_segments = []
    current_pos = topic_start
    for b_s, b_e in merged_blocks:
        if current_pos < b_s:
            result_segments.append((current_pos, b_s - datetime.timedelta(days=1)))
        current_pos = b_e + datetime.timedelta(days=1)
    if current_pos <= topic_end:
        result_segments.append((current_pos, topic_end))
    return result_segments

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
    # Add your persistence logic here if needed
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

def reschedule_dsa(entries, new_topic=None, delete_uid=None):
    events = copy.deepcopy(entries)

    if delete_uid:
        events = [e for e in events if e['UID'] != delete_uid]

    breaks = [e for e in events if e["Type"] == "Break"]
    dsa = [e for e in events if e["Type"] == "DSA"]

    break_intervals = []
    for b in breaks:
        for _, s, e in expand_all_ranges([b]):
            break_intervals.append((s, e))
    break_intervals.sort()

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

    locked_intervals = [*[(s, e, b) for b, s, e in [(b,) + bi for bi in break_intervals]]]
    for ni in new_topic_intervals:
        locked_intervals.append(ni)
    locked_intervals.sort(key=lambda x: x[0])

    topic_splits_count = {}

    def earliest_start(r):
        drs = r["Date Range"].split(",")
        starts = [parse_date(d.split("–")[0].strip()) for d in drs]
        return min(starts)

    dsa_sorted = sorted(dsa, key=earliest_start)

    scheduled = []

    for topic in dsa_sorted:
        if new_topic and topic["Topic"] == new_topic['topic']:
            segs = [(new_topic['start'], new_topic['end'])]
        else:
            segs_orig = []
            for _, s, e in expand_all_ranges([topic]):
                segs_orig.append((s, e))
            segs = []
            for seg in segs_orig:
                segments = split_topic_by_breaks(seg, break_intervals)
                segs.extend(segments)

        for idx_seg, (seg_start, seg_end) in enumerate(segs):
            key = topic['Topic']
            topic_splits_count[key] = topic_splits_count.get(key, 0) + 1
            split_num = topic_splits_count[key]

            display_topic = f"{topic['Topic']} (part {split_num})" if len(segs) > 1 else topic['Topic']
            days = days_between(seg_start, seg_end)
            uid = get_uid()

            scheduled.append({
                "S No.": 0,
                "Type": "DSA",
                "Topic": display_topic,
                "Days": days,
                "Date Range": daterange_fmt(seg_start, seg_end),
                "Notes": topic.get("Notes", ""),
                "UID": uid
            })

    for b in breaks:
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

    def start_date(ev):
        return parse_date(ev["Date Range"].split("–")[0].strip())

    scheduled.sort(key=start_date)

    if new_topic:
        new_s = new_topic['start']
        new_e = new_topic['end']

        for ev in scheduled:
            if ev["Type"] == "DSA":
                ev_start = parse_date(ev["Date Range"].split("–")[0].strip())
                ev_end = parse_date(ev["Date Range"].split("–")[-1].strip())
                if ev_start <= new_e and ev_end >= new_s:
                    new_start = new_e + datetime.timedelta(days=1)
                    days = ev["Days"]
                    ev["Date Range"] = daterange_fmt(new_start, new_start + datetime.timedelta(days=days - 1))

    for idx, ev in enumerate(scheduled, 1):
        ev["S No."] = idx

    return scheduled

def main():
    st.title("📅 DSA Sheet Scheduler (Daily App)")
    st.info("Add study topics, breaks, or fun/wasted events below! Schedule splits topics only at breaks. Breaks stay fixed. Delete or add rows as needed.")

    st.session_state.dsa_sheet = reschedule_dsa(st.session_state.dsa_sheet)
    df = pd.DataFrame(st.session_state.dsa_sheet)

    if not df.empty:
        st.subheader("DSA Schedule Table")
        show_df = df.drop(columns=["UID"])
        st.dataframe(show_df, use_container_width=True)

        st.markdown("### Delete any row:")
        for i, row in df.iterrows():
            col1, col2 = st.columns([8, 2])
            s_no = row.get('S No.', i + 1)
            col1.markdown(f"**{s_no}. {row['Type']} — {row['Topic']}** ({row['Date Range']})")
            delete_clicked = col2.button(f"🗑️ Delete", key=f"del_{row['UID']}_{i}")
            if delete_clicked:
                st.session_state.dsa_sheet = reschedule_dsa(st.session_state.dsa_sheet, delete_uid=row['UID'])
                _save_data()
                st.experimental_rerun()
                return

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
            return

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
            st.session_state.dsa_sheet = reschedule_dsa(st.session_state.dsa_sheet)
            _save_data()
            st.success("Added new Break/Fun activity!")
            st.experimental_rerun()
            return

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
            return

    st.markdown("---")
    st.markdown("Made with ❤️ for efficient DSA prep! [Perplexity AI App Example]")

if __name__ == "__main__":
    main()
