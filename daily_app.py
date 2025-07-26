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

def days_between(start, end):
    if isinstance(start, pd.Timestamp):
        start = start.date()
    if isinstance(end, pd.Timestamp):
        end = end.date()
    return (end - start).days + 1

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

DEFAULT_DATA = [
    {"Type": "DSA", "Topic": "LinkedList", "Days": 11, "Date Range": "25/08/25 – 04/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Sorting", "Days": 8, "Date Range": "05/09/25 – 12/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "1day break", "Days": 1, "Date Range": "13/09/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Dynamic Prog", "Days": 18, "Date Range": "14/09/25 – 01/10/25", "Notes": "", "UID": get_uid()},
    {"Type": "Break", "Topic": "CAT-1", "Days": 11, "Date Range": "02/10/25 – 12/10/25", "Notes": "", "UID": get_uid()},
    {"Type": "DSA", "Topic": "Graphs", "Days": 21, "Date Range": "13/10/25 – 02/11/25", "Notes": "", "UID": get_uid()},
]

if "dsa_sheet" not in st.session_state:
    st.session_state.dsa_sheet = copy.deepcopy(DEFAULT_DATA)

def _save_data():
    pass  # persistence placeholder

def expand_date_ranges(row):
    """Returns list of (start_date, end_date) for a row with possibly multiple date ranges (comma separated)."""
    drs = row["Date Range"].split(",")
    ranges = []
    for dr in drs:
        dr = dr.strip()
        if "–" in dr:
            parts = dr.split("–")
            start = parse_date(parts[0].strip())
            end = parse_date(parts[1].strip())
        else:
            start = end = parse_date(dr)
        if start and end:
            ranges.append((start, end))
    return ranges

def intervals_overlap(start1, end1, start2, end2):
    """Return True if intervals [start1, end1] and [start2, end2] overlap."""
    return start1 <= end2 and start2 <= end1

def split_interval_by_interval(outer_start, outer_end, inner_start, inner_end):
    """
    Given outer interval and inner interval (that may overlap),
    return list of intervals for outer interval excluding inner interval.
    Result: 0 to 2 intervals, non-overlapping, in order.
    """
    result = []
    if inner_start > outer_start:
        # segment before inner interval
        result.append((outer_start, prev_day(inner_start)))
    if inner_end < outer_end:
        # segment after inner interval
        result.append((next_day(inner_end), outer_end))
    return result

def reschedule_with_interruptions(entries, new_topic=None, delete_uid=None):
    events = copy.deepcopy(entries)
    if delete_uid:
        events = [e for e in events if e['UID'] != delete_uid]

    breaks = [e for e in events if e["Type"] == "Break"]
    dsa = [e for e in events if e["Type"] == "DSA"]

    # Collect break intervals (fixed)
    break_intervals = []
    for br in breaks:
        for bstart, bend in expand_date_ranges(br):
            break_intervals.append((bstart, bend))
    break_intervals.sort()

    def is_break_day(date):
        for bstart, bend in break_intervals:
            if bstart <= date <= bend:
                return True
        return False

    # Prepare new topic interval if any
    new_topic_range = None
    if new_topic:
        new_topic_range = (new_topic['start'], new_topic['end'])

    # === STEP 1: Build timeline chunks ===
    # We want to split existing DSA topics by the new topic's interval, and by breaks
    # All break periods are fixed, so will remain as-is

    # We'll process all DSA topics, splitting them as needed:
    # - First, if new_topic is inserted, split existing topics overlapping new topic
    # - Second, split all topics by breaks (keep breaks fixed)
    # - Finally, flatten into list of non-overlapping intervals

    split_chunks = []  # List of dicts with keys: Type, Topic, Days, Date Range, Notes, UID, PartNo, TotalParts, DayStart, DayEnd

    # We process DSA topics sorted by earliest start date (for consistent ordering)
    def get_earliest_start(ev):
        starts = [s for s, e in expand_date_ranges(ev)]
        return min(starts) if starts else datetime.date.today()
    dsa_sorted = sorted(dsa, key=get_earliest_start)

    for topic in dsa_sorted:
        topic_ranges = expand_date_ranges(topic)

        # list to accumulate split segments for this topic
        topic_segments = []

        for tstart, tend in topic_ranges:

            # First, if new topic exists and overlaps this segment, break current into max 2 parts
            if new_topic_range and intervals_overlap(tstart, tend, new_topic_range[0], new_topic_range[1]):
                # calculate parts excluding new topic interval
                split_before_after = split_interval_by_interval(tstart, tend, new_topic_range[0], new_topic_range[1])
            else:
                split_before_after = [(tstart, tend)]

            # For each part after splitting by new topic, further split by breaks
            for seg_start, seg_end in split_before_after:
                # If this segment is empty, skip
                if seg_start > seg_end:
                    continue

                # Split by breaks:
                # We split by breaks: break intervals are fixed and DSA not scheduled during breaks
                # So DSA parts only on date ranges excluding breaks
                # We implement splitting by subtracting break intervals from [seg_start, seg_end]
                current_start = seg_start
                while current_start <= seg_end:
                    # Find next break overlapping current_start
                    next_break = None
                    for bstart, bend in break_intervals:
                        if bstart <= seg_end and bend >= current_start:
                            # break overlaps current segment's remainder
                            if bstart > current_start:
                                # free segment before break
                                free_seg_end = prev_day(bstart)
                            else:
                                # current_start inside break, skip break
                                current_start = next_day(bend)
                                break
                            next_break = (bstart, bend)
                            break
                    else:
                        # No break found overlapping current_start
                        free_seg_end = seg_end
                        next_break = None

                    if current_start <= free_seg_end:
                        # This is a free segment part inside this topic
                        topic_segments.append((current_start, free_seg_end))
                        current_start = next_day(free_seg_end)
                    else:
                        if next_break is None:
                            # no next break at all remain
                            break
                        # skip the break interval
                        current_start = next_day(next_break[1])

        # Now topic_segments contains disjoint non-break date intervals for this topic (excluding new_topic overlap)

        # Sort and assign part numbers
        topic_segments = sorted(topic_segments)
        total_parts = len(topic_segments)
        for idx, (ps, pe) in enumerate(topic_segments, 1):
            days_len = days_between(ps, pe)
            # Prepare UID for splitting (can associate with original topic UID for reference)
            uid = get_uid()

            display_topic = topic['Topic']
            # Add part suffix if more than one part
            if total_parts > 1:
                display_topic = f"{display_topic} (part {idx} of {total_parts})"

            split_chunks.append({
                "Type": "DSA",
                "Topic": display_topic,
                "Days": days_len,
                "Date Range": daterange_fmt(ps, pe),
                "Notes": topic.get("Notes", ""),
                "UID": uid,
                "OrigUID": topic.get("UID"),
                "Start": ps,
                "End": pe,
            })

    # Add the new topic as separate chunk (if any)
    if new_topic:
        days_len = days_between(new_topic['start'], new_topic['end'])
        split_chunks.append({
            "Type": "DSA",
            "Topic": new_topic['topic'],
            "Days": days_len,
            "Date Range": daterange_fmt(new_topic['start'], new_topic['end']),
            "Notes": new_topic.get("note", ""),
            "UID": get_uid(),
            "Start": new_topic['start'],
            "End": new_topic['end'],
        })

    # Append break intervals as fixed schedule items
    for br in breaks:
        ranges = expand_date_ranges(br)
        for bstart, bend in ranges:
            days_len = days_between(bstart, bend)
            split_chunks.append({
                "Type": "Break",
                "Topic": br["Topic"],
                "Days": days_len,
                "Date Range": daterange_fmt(bstart, bend),
                "Notes": br.get("Notes", ""),
                "UID": br.get("UID", get_uid()),
                "Start": bstart,
                "End": bend,
            })

    # Sort all by start date
    split_chunks.sort(key=lambda x: x["Start"])

    # === Consolidate consecutive parts with same Topic & Type if adjacent === (optional)
    consolidated = []
    for seg in split_chunks:
        if consolidated:
            last = consolidated[-1]
            if (seg["Type"] == last["Type"] and seg["Topic"] == last["Topic"] and
                (last["End"] + datetime.timedelta(days=1)) == seg["Start"]):
                # Merge segments
                last["End"] = seg["End"]
                last["Days"] = days_between(last["Start"], last["End"])
                last["Date Range"] = daterange_fmt(last["Start"], last["End"])
                # Concatenate Notes? Optional, keep first for now
                continue
        consolidated.append(seg)

    # Assign serial numbers with part numbering for original topic grouping

    # Build map: topic -> list of segments
    topic_groups = {}
    for ev in consolidated:
        key = (ev["Type"], ev["Topic"])
        topic_groups.setdefault(key, []).append(ev)

    # For DSA topics, add numbering like 1.1, 1.2 etc by topic group ordering
    # First, order topic groups by earliest start date
    topic_order = sorted(topic_groups.keys(), key=lambda k: min(ev["Start"] for ev in topic_groups[k]))

    result = []
    current_sno = 1
    for group_idx, grp_key in enumerate(topic_order, 1):
        evs = topic_groups[grp_key]
        if grp_key[0] == "DSA":
            # Number parts for DSA
            total_parts = len(evs)
            for part_idx, ev in enumerate(evs, 1):
                part_suffix = ""
                # If total_parts>1, swap topic name to remove previous part info (if any)
                base_topic = ev["Topic"].split(" (part ")[0].strip()
                if total_parts > 1:
                    part_suffix = f"{part_idx} of {total_parts}"
                    ev["Topic"] = f"{base_topic} ({part_suffix})"
                else:
                    ev["Topic"] = base_topic

                ev["S No."] = f"{group_idx}.{part_idx}"
                result.append(ev)
        else:
            # No part numbering for breaks
            ev = evs[0]
            ev["S No."] = str(group_idx)
            result.append(ev)

    return result


def main():
    st.title("📅 DSA Sheet Scheduler with Interruptive Rescheduling")

    st.info(
        "Add a new DSA study topic to split (interrupt) existing topics as per dates entered.\n"
        "Breaks are fixed and preserved.\n"
        "Deletions and additions auto-update the schedule."
    )

    # Reschedule and assign serial numbers
    st.session_state.dsa_sheet = reschedule_with_interruptions(st.session_state.dsa_sheet)
    df = pd.DataFrame(st.session_state.dsa_sheet)

    if not df.empty:
        st.subheader("DSA Schedule Table")
        st.dataframe(df.drop(columns=["UID", "Start", "End"]), use_container_width=True)

        st.markdown("### Delete any row:")
        for idx, row in df.iterrows():
            col1, col2 = st.columns([9, 1])
            col1.markdown(f"**{row['S No.']} {row['Type']} — {row['Topic']}** ({row['Date Range']})")
            if col2.button("🗑️ Delete", key=f"del_{row['UID']}"):
                st.session_state.dsa_sheet = reschedule_with_interruptions(st.session_state.dsa_sheet, delete_uid=row['UID'])
                _save_data()
                st.rerun()
                return
    else:
        st.info("No DSA schedule entries yet.")

    st.markdown("---")
    st.subheader("Add Study Topic")

    today = datetime.date.today()

    with st.form("add_study_form"):
        study_topic = st.text_input("Topic (e.g. LinkedList)", value="", key="input_topic")
        study_from = st.date_input("From Date", value=today, key="input_from")
        study_to = st.date_input("To Date", value=today, key="input_to")
        study_notes = st.text_input("Notes (optional)", value="✅ Manually Added", key="input_note")
        submitted = st.form_submit_button("➕ Add Study Topic")

    if submitted:
        if not study_topic.strip():
            st.error("Please enter a study topic.")
        elif study_from > study_to:
            st.error("From date cannot be after To date.")
        else:
            new_topic_input = {
                "topic": study_topic.strip(),
                "start": study_from,
                "end": study_to,
                "note": study_notes.strip(),
            }
            st.session_state.dsa_sheet = reschedule_with_interruptions(st.session_state.dsa_sheet, new_topic=new_topic_input)
            _save_data()
            st.success(f"Added study topic '{study_topic.strip()}' and rescheduled.")
            st.rerun()
            return

    st.markdown("---")
    st.markdown("Made with ❤️ for efficient DSA prep!")

# Always run main() at global scope for Streamlit
main()
