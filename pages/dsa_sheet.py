import streamlit as st
import pandas as pd
import datetime
from copy import deepcopy
from core.data_handler import save_data

def draw():
    st.title("🧠 DSA Sheet Scheduling")
    FIXED_KEYWORDS = ["CAT", "Gravitas"]

    today = datetime.date.today()

    # ---- SESSION STATE INIT ----
    if "dsa_sheet" not in st.session_state or not isinstance(st.session_state.dsa_sheet, list):
        st.session_state.dsa_sheet = []

    if "delete_latest_confirm" not in st.session_state:
        st.session_state.delete_latest_confirm = False
    if "delete_action_flag" not in st.session_state:
        st.session_state.delete_action_flag = False

    # --- Helpers for dates and breaks ---
    def parse_date(date_str):
        return datetime.datetime.strptime(date_str, "%d/%m/%y").date()
    def format_date(date):
        return date.strftime("%d/%m/%y")
    def format_date_range(start, end):
        if start == end:
            return format_date(start)
        return f"{format_date(start)} – {format_date(end)}"
    def daterange(start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + datetime.timedelta(n)
    
    def is_break(topic_row):
        typ = topic_row.get('Type', '')
        topic = topic_row.get('Topic', '')
        if typ.lower() == "break":
            return True
        if any(kw.lower() in topic.lower() for kw in FIXED_KEYWORDS):
            return True
        # Covers #P... style
        if topic.startswith("#P"):
            return True
        return False
    
    # --- Parse DSA sheet entries' date ranges ---
    def parse_row_range(row):
        # Support single range or composite ("14/10/25 – 16/10/25, 19/10/25 – 25/10/25")
        dr = row['Date Range']
        periods = []
        for rng in dr.split(','):
            rng = rng.strip()
            if "–" in rng:
                part = rng.split("–")
                start, end = part[0].strip(), part[1].strip()
                periods.append((parse_date(start), parse_date(end)))
            else:
                dt = parse_date(rng.strip())
                periods.append((dt, dt))
        return periods

    # --- Find all break periods (returns list of (start,end) tuples) ---
    def get_break_periods(sheet):
        periods = []
        for row in sheet:
            if is_break(row):
                periods += parse_row_range(row)
        return periods

    # --- Schedule window utility: returns next date available for DSA/skippable task, given a start, skipping through the breaks ---
    def find_next_available(start_date, days, break_periods):
        current = start_date
        assigned = 0
        periods = []
        while assigned < days:
            # Skip if in a break
            in_break = False
            for bstart, bend in break_periods:
                if bstart <= current <= bend:
                    current = bend + datetime.timedelta(days=1)
                    in_break = True
                    break
            if not in_break:
                # Find maximal continuous slot (before next break, or for 'days-assigned')
                days_here = 1
                while (
                    assigned + days_here < days
                    and not any(
                        bstart <= current + datetime.timedelta(days=days_here) <= bend
                        for bstart, bend in break_periods
                    )
                ):
                    days_here += 1
                periods.append( (current, current + datetime.timedelta(days=days_here - 1)) )
                assigned += days_here
                current = current + datetime.timedelta(days=days_here)
        return periods

    # --- Given a schedule, split/shift DSA topics as needed, with breaks fixed ---
    def rebuild_schedule_with_new(sheet, new_entry=None, delete_row_idx=None):
        """
        - sheet: list of current rows (dicts).
        - new_entry: Optional dict for new topic. If None, means just to repack after delete.
        - delete_row_idx: Optional index to delete, before rescheduling.
        Returns: new (list of dicts), with all DSA topics fit around breaks.
        """
        # 1. Remove delete_row if needed
        scratch = deepcopy(sheet)
        if delete_row_idx is not None:
            if delete_row_idx < len(scratch):
                del scratch[delete_row_idx]

        # 2. Load all breaks (fixed)
        breaks = []
        moving_dsas = []
        for row in scratch:
            if is_break(row):
                # Keep as is
                breaks.append(row)
            else:
                moving_dsas.append(row)

        # 3. Insert new DSA topic, if provided (before reschedule/pack)
        inserted = False
        if new_entry is not None:
            # Identify point to insert (by date), and handle split
            # We model 'moving_dsas' as flat list, each as (topic row)
            packed = []
            placed = False
            for row in moving_dsas:
                # For each row, see if its range overlaps new_entry range
                orig_periods = parse_row_range(row)
                all_days = []
                for rng in orig_periods:
                    rng_days = list(daterange(rng[0], rng[1]))
                    all_days += rng_days
                # Now, the days for the new entry
                new_days = list(daterange(new_entry['Start'], new_entry['End']))
                overlap = sorted(set(all_days) & set(new_days))
                if not overlap:
                    packed.append(row)
                    continue
                # Need to split this row into up to two:
                days_before = [d for d in all_days if d < new_entry['Start']]
                days_after = [d for d in all_days if d > new_entry['End']]
                if days_before:
                    part1 = deepcopy(row)
                    part1['Topic'] = f"{row['Topic']} (Part 1)"
                    part1['Days'] = len(days_before)
                    part1['Date Range'] = format_date_range(days_before[0], days_before[-1])
                    packed.append(part1)
                # The new entry itself is added immediately after this (if not yet done)
                if not placed:
                    packed.append({
                        "Type": new_entry['Type'] if new_entry.get('Type') else "DSA",
                        "Topic": new_entry['Topic'],
                        "Days": (new_entry['End'] - new_entry['Start']).days + 1,
                        "Date Range": format_date_range(new_entry['Start'], new_entry['End']),
                        "Notes": new_entry.get('Notes', '–')
                    })
                    placed = True
                if days_after:
                    part2 = deepcopy(row)
                    part2['Topic'] = f"{row['Topic']} (continued)"
                    part2['Days'] = len(days_after)
                    part2['Date Range'] = format_date_range(days_after[0], days_after[-1])
                    packed.append(part2)
            # Add any remaining DSA topics after where we've inserted
            if not placed:
                # Insert at end if no overlap at all
                packed.append({
                    "Type": new_entry['Type'] if new_entry.get('Type') else "DSA",
                    "Topic": new_entry['Topic'],
                    "Days": (new_entry['End'] - new_entry['Start']).days + 1,
                    "Date Range": format_date_range(new_entry['Start'], new_entry['End']),
                    "Notes": new_entry.get('Notes', '–')
                })
            moving_dsas = packed
        # 4. Repack all DSA topics into available slots (skipping over breaks)
        # Gather desired number of days for each, keep their 'Topic', 'Notes', etc.
        dsa_tasks = []
        for row in moving_dsas:
            # flatten possible composite ranges
            days = row['Days']
            name = row['Topic']
            notes = row.get('Notes', "")
            typ = row.get('Type', "DSA")
            dsa_tasks.append({'Type': typ, 'Topic': name, 'Days': days, 'Notes': notes})

        # Sort breaks chronologically
        ordered_breaks = sorted(
            breaks,
            key=lambda r: parse_row_range(r)[0][0] if len(parse_row_range(r)) else datetime.date(2099,1,1)
        )
        # Find first available date (after all prior breaks)
        all_break_periods = get_break_periods(ordered_breaks)
        current = ordered_breaks[0] if ordered_breaks else None
        first_date = min(
            [
                row for row in ordered_breaks
                if parse_row_range(row)
            ],
            key=lambda r: parse_row_range(r)[0][0]
        ) if ordered_breaks else None
        earliest = (
            parse_row_range(first_date)[0][0]
            if first_date
            else today
        )
        # But let DSA topics start at the earliest available date (or even before first break)
        current_date = earliest if new_entry is None else min(new_entry.get('Start', earliest), earliest)
        # Actually, run through all scheduled periods (breaks), assign as possible
        filled = []
        # Re-detect all break periods
        break_periods = get_break_periods(ordered_breaks)
        dsa_counter = 1
        for task in dsa_tasks:
            avail_periods = find_next_available(current_date, task['Days'], break_periods)
            # Recompose row as usual, possibly in multiple ranges (if interrupted by breaks)
            # If composite, show ranges as "A – B, C – D,..."
            full_range = ", ".join(format_date_range(a, b) for a, b in avail_periods)
            row = {
                "Type": task['Type'],
                "Topic": task['Topic'],
                "Days": task['Days'],
                "Date Range": full_range,
                "Notes": task['Notes'],
            }
            filled.append(row)
            # Next available date is the day after the last date just assigned
            current_date = avail_periods[-1][1] + datetime.timedelta(days=1)
            dsa_counter += 1
        # Merge with fixed breaks, all in chronological order
        all_rows = filled + ordered_breaks
        all_rows = sorted(
            all_rows,
            key=lambda r: parse_row_range(r)[0][0] if len(parse_row_range(r)) else datetime.date(2099,1,1)
        )
        # Add row numbers/# for display
        for idx, row in enumerate(all_rows):
            row["#"] = idx+1
        return all_rows

    # --- Handle per-row delete interactions ---
    delete_triggered = None
    if "delete_row_idx" not in st.session_state:
        st.session_state.delete_row_idx = None

    # --- TABLE DISPLAY & ROW DELETE ---
    current_table = deepcopy(st.session_state.dsa_sheet)
    tab_data = []
    for idx, row in enumerate(current_table):
        displayed_row = dict(row)
        displayed_row["🗑️"] = ""
        tab_data.append(displayed_row)
    df = pd.DataFrame(tab_data)
    def highlight_breaks(row):
        return ['background-color: #D0E7FF' if row['Type']=='Break' else '' for _ in row]
    st.markdown("### DSA Schedule with Notes (Editable & Deletable)")
    # Render custom table with buttons
    # Each row: columns (data | btn)
    for idx, row in enumerate(current_table):
        cols = st.columns([18,1])
        with cols[0]:
            st.write(
                f"**[{row.get('Type','')}] {row.get('Topic','')}**\n\n"
                f"Days: {row.get('Days', '')} | Date Range: {row.get('Date Range', '')} | Notes: {row.get('Notes','')}"
            )
        with cols[1]:
            if st.button("🗑️ Delete", key=f"delrow_{idx}"):
                st.session_state.delete_row_idx = idx
                delete_triggered = idx
                break   # After rerun, session will reload
    if st.session_state.delete_row_idx is not None:
        # On deletion, recalc
        st.session_state.dsa_sheet = rebuild_schedule_with_new(
            st.session_state.dsa_sheet,
            new_entry=None,
            delete_row_idx=st.session_state.delete_row_idx
        )
        st.session_state.delete_row_idx = None
        save_data()
        st.success("Topic deleted and schedule repacked!")
        st.experimental_rerun()

    if not st.session_state.dsa_sheet:
        st.info("No DSA entries found yet. Add one using options below.")

    # ---------- DELETE LATEST ENTRY BUTTON (with confirmation) ------------
    if st.session_state.dsa_sheet:
        if not st.session_state.delete_latest_confirm:
            if st.button("🗑️ Delete Latest Entry"):
                st.session_state.delete_latest_confirm = True
        else:
            st.warning("Are you sure you want to delete the latest entry? This cannot be undone.")
            col1, col2 = st.columns(2)
            yes_clicked = col1.button("✅ Yes, Delete", key="yes_latest")
            cancel_clicked = col2.button("❌ Cancel", key="cancel_latest")
            if yes_clicked:
                st.session_state.delete_action_flag = True
                st.session_state.delete_latest_confirm = False
            elif cancel_clicked:
                st.session_state.delete_latest_confirm = False

    if st.session_state.delete_action_flag:
        if st.session_state.dsa_sheet:
            st.session_state.dsa_sheet.pop()
            st.session_state.dsa_sheet = rebuild_schedule_with_new(
                st.session_state.dsa_sheet
            )
            save_data()
            st.success("Latest entry deleted!")
        else:
            st.warning("No entries to delete.")
        st.session_state.delete_action_flag = False
        st.experimental_rerun()

    # ------------------ SAVE NOTES -------------------
    # (If editing of notes via UI is required)
    if st.session_state.dsa_sheet:
        if st.button("💾 Save Notes"):
            # For now, no editable field per row - see pandas editable hack for full interactive editing
            save_data()
            st.success("Notes saved successfully!")

    # -------------- INPUT BARS BELOW ------------------
    st.markdown("<div style='background:#e9ffe9;padding:15px;margin-top:10px;border-radius:8px;'>"
                "<h4>🟩 Add Study (Green Bar)</h4>", unsafe_allow_html=True)
    g1, g2 = st.columns(2)
    green_topic = g1.text_input("Topic You Studied / Completed", key="green_topic")
    green_from = g2.date_input("From", key="green_from", value=today)
    green_to = g2.date_input("Till", key="green_to", value=today+datetime.timedelta(days=1))
    green_notes = g1.text_input("Any Notes (optional)", key="green_notes")
    if st.button("➕ GO - Add Study"):
        if green_topic and green_from <= green_to:
            new_entry = {
                "Type": "DSA",
                "Topic": green_topic,
                "Start": green_from,
                "End": green_to,
                "Notes": green_notes or "✅ Manually Added"
            }
            st.session_state.dsa_sheet = rebuild_schedule_with_new(
                st.session_state.dsa_sheet,
                new_entry=new_entry
            )
            save_data()
            st.success(f"Added topic: {green_topic}")
            st.experimental_rerun()
        else:
            st.warning("Check topic and date range!")

    # 🟥 RED BAR – Fun Break
    st.markdown("<div style='background:#ffeaea;padding:15px;margin-top:10px;border-radius:8px;'>"
                "<h4>🟥 Add Fun Activity (Red Bar)</h4>", unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    red_topic = r1.text_input("Fun You Did (e.g. Movie, Sports)", key="red_topic")
    red_from = r2.date_input("From", key="red_from", value=today)
    red_to = r2.date_input("Till", key="red_to", value=today+datetime.timedelta(days=1))
    if st.button("➕ GO - Add Fun"):
        if red_topic and red_from <= red_to:
            # Direct append, breaks never shift
            break_row = {
                "Type": "Break",
                "Topic": red_topic,
                "Days": (red_to - red_from).days + 1,
                "Date Range": format_date_range(red_from, red_to),
                "Notes": "🎈 Fun/Enjoyment"
            }
            st.session_state.dsa_sheet.append(break_row)
            # No reschedule needed for breaks
            st.session_state.dsa_sheet = rebuild_schedule_with_new(st.session_state.dsa_sheet)
            save_data()
            st.success(f"Added fun: {red_topic}")
            st.experimental_rerun()
        else:
            st.warning("Please enter fun topic and valid date range.")

    # ⬜ GRAY BAR – Wasted Time
    st.markdown("<div style='background:#f0f0f0;padding:15px;margin-top:10px;border-radius:8px;'>"
                "<h4>⬜ Add Wasted Time (Gray Bar)</h4>", unsafe_allow_html=True)
    y1, y2 = st.columns(2)
    gray_reason = y1.text_input("Wasted Time Reason", key="gray_reason")
    gray_from = y2.date_input("From", key="gray_from", value=today)
    gray_to = y2.date_input("Till", key="gray_to", value=today+datetime.timedelta(days=1))
    if st.button("➕ GO - Add Wasted Time"):
        if gray_reason and gray_from <= gray_to:
            # Direct append, breaks never shift
            break_row = {
                "Type": "Break",
                "Topic": gray_reason,
                "Days": (gray_to - gray_from).days + 1,
                "Date Range": format_date_range(gray_from, gray_to),
                "Notes": "😓 Time Wasted"
            }
            st.session_state.dsa_sheet.append(break_row)
            st.session_state.dsa_sheet = rebuild_schedule_with_new(st.session_state.dsa_sheet)
            save_data()
            st.success(f"Logged wasted time: {gray_reason}")
            st.experimental_rerun()
        else:
            st.warning("Please enter a reason and date range.")

    # Save data on initial load if needed
    save_data()





