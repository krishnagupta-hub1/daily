import streamlit as st
import pandas as pd
import datetime
import uuid
import copy

st.set_page_config(page_title="DSA Daily Scheduler", layout="wide")

####### ---------- HELPER FUNCTIONS ------------- #######

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

###### --------- DATA AND INITIALIZATION ---------- ######

DEFAULT_DATA = [
    # Your initial schedule entries
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
    # Placeholder for persistence logic
    pass

###### ---------- ADVANCED RESCHEDULING CORE ---------- ######

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

def reschedule_dsa_with_interruptions(entries, new_topic=None, delete_uid=None):
    events = copy.deepcopy(entries)
    if delete_uid:
        events = [e for e in events if e['UID'] != delete_uid]

    breaks = [e for e in events if e["Type"] == "Break"]
    dsa = [e for e in events if e["Type"] == "DSA"]

    all_dates = []
    for r, s, e in expand_all_ranges(events):
        all_dates.append(s)
    base_date = min(all_dates) if all_dates else datetime.date.today()

    locked = []
    for b in breaks:
        for _, s, e in expand_all_ranges([b]):
            locked.append((s, e, b))

    interruptions = []
    if new_topic:
        interruptions.append((
            new_topic['start'], new_topic['end'], {
                "Type": "DSA",
                "Topic": new_topic['topic'],
                "Days": (new_topic['end'] - new_topic['start']).days + 1,
                "Date Range": daterange_fmt(new_topic['start'], new_topic['end']),
                "Notes": new_topic.get('note', ""),
                "UID": get_uid(),
            }
        ))

    all_dsa_segments = []
    for d in dsa:
        for _, start, end in expand_all_ranges([d]):
            length = (end - start).days + 1
            all_dsa_segments.extend([{
                "Topic": d["Topic"],
                "UID": d["UID"],
                "Notes": d.get("Notes", ""),
            }] * length)

    protected_days_map = {}
    for s, e, ev in locked + interruptions:
        d = s
        while d <= e:
            protected_days_map[d] = ev
            d = next_day(d)

    output = []
    current_date = base_date
    dsa_pointer = 0
    dsa_topic_counts = {}

    while dsa_pointer < len(all_dsa_segments) or current_date in protected_days_map:
        if current_date in protected_days_map:
            ev = protected_days_map[current_date]
            if output and output[-1]['UID'] == ev['UID']:
                output[-1]['Days'] += 1
                start_str = output[-1]['Date Range'].split('–')[0].strip()
                start_dt = parse_date(start_str)
                output[-1]['Date Range'] = daterange_fmt(start_dt, current_date)
            else:
                new_event = copy.deepcopy(ev)
                new_event['Days'] = 1
                new_event['Date Range'] = daterange_fmt(current_date, current_date)
                if 'Type' not in new_event:
                    new_event['Type'] = "Break"
                if 'UID' not in new_event:
                    new_event['UID'] = get_uid()
                output.append(new_event)
            current_date = next_day(current_date)
            continue

        if dsa_pointer >= len(all_dsa_segments):
            break

        seg = all_dsa_segments[dsa_pointer]
        topic_name = seg["Topic"]
        dsa_topic_counts[topic_name] = dsa_topic_counts.get(topic_name, 0) + 1
        part_num = dsa_topic_counts[topic_name]
        if part_num == 1:
            display_topic = topic_name
        else:
            display_topic = f"{topic_name} (continued {part_num})"

        if output and output[-1]['Type'] == "DSA" and output[-1]["Topic"] == display_topic:
            output[-1]['Days'] += 1
            start_str = output[-1]['Date Range'].split('–')[0].strip()
            start_dt = parse_date(start_str)
            output[-1]['Date Range'] = daterange_fmt(start_dt, current_date)
        else:
            output.append({
                "S No.": 0,
                "Type": "DSA",
                "Topic": display_topic,
                "Days": 1,
                "Date Range": daterange_fmt(current_date, current_date),
                "Notes": seg.get("Notes", ""),
                "UID": get_uid()
            })
        dsa_pointer += 1
        current_date = next_day(current_date)

    if output:
        last_date_str = output[-1]['Date Range'].split('–')[-1].strip()
        last_date = parse_date(last_date_str)
    else:
        last_date = base_date

    extra_locked_days = []
    for s, e, ev in locked + interruptions:
        d = s
        while d <= e:
            if d > last_date and d not in protected_days_map:
                extra_locked_days.append((d, ev))
            d = next_day(d)

    extra_locked_days.sort(key=lambda x: x[0])
    for d, ev in extra_locked_days:
        if output and output[-1].get("UID") == ev.get("UID"):
            output[-1]['Days'] += 1
            start_dt = parse_date(output[-1]['Date Range'].split('–')[0].strip())
            output[-1]['Date Range'] = daterange_fmt(start_dt, d)
        else:
            new_ev = copy.deepcopy(ev)
            new_ev['Days'] = 1
            new_ev['Date Range'] = daterange_fmt(d, d)
            if 'Type' not in new_ev:
                new_ev['Type'] = "Break"
            if 'UID' not in new_ev:
                new_ev['UID'] = get_uid()
            output.append(new_ev)

    output.sort(key=lambda x: parse_date(x["Date Range"].split("–")[0].strip()))

    for idx, ev in enumerate(output, 1):
        ev["S No."] = idx

    return output

###### ----------- MAIN APP UI & LOGIC ----------- #######

def main():
    st.title("📅 DSA Sheet Scheduler (Daily App)")

    st.info("Add study topics, breaks, or fun/wasted events below! Your DSA schedule will split/reschedule automatically to avoid date overlaps. Breaks stay fixed. You can delete any row. 'Save Notes' will store notes for each row.")

    # **Ensure schedule is always freshly rescheduled and S No. assigned**
    st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(st.session_state.dsa_sheet)
    df = pd.DataFrame(st.session_state.dsa_sheet)

    if not df.empty:
        st.subheader("DSA Schedule Table")

        # Display schedule table without UID column
        show_df = df.drop(columns=["UID"])
        st.dataframe(show_df, use_container_width=True)

        # Delete row buttons per entry
        st.markdown("### Delete any row:")
        for i, row in df.iterrows():
            col1, col2 = st.columns([8, 2])
            s_no = row['S No.'] if 'S No.' in row else i + 1
            col1.markdown(f"**{s_no}. {row['Type']} — {row['Topic']}** ({row['Date Range']})")
            if col2.button(f"🗑️ Delete", key=f"del_{row['UID']}"):
                st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(
                    st.session_state.dsa_sheet,
                    new_topic=None,
                    delete_uid=row['UID']
                )
                _save_data()
                st.experimental_rerun()
    else:
        st.info("No DSA entries yet.")

    # ------ Add Entry Forms ------
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
            st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(
                st.session_state.dsa_sheet,
                new_topic=dict(
                    topic=study_topic.strip(),
                    start=study_from,
                    end=study_to,
                    note=study_note.strip()
                )
            )
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
            st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(st.session_state.dsa_sheet)
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
            st.session_state.dsa_sheet = reschedule_dsa_with_interruptions(st.session_state.dsa_sheet)
            _save_data()
            st.success("Logged wasted time as Break!")
            st.experimental_rerun()

    st.markdown("---")
    st.markdown("Made with ❤️ for efficient DSA prep! [Perplexity AI App Example]")

if __name__ == "__main__":
    main()
