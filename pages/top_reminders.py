import streamlit as st
import datetime

def draw():
    st.title("🔔 Top Reminders")

    # Initialize reminders in session_state if not present
    if "top_reminders" not in st.session_state:
        st.session_state.top_reminders = []

    # Input section: reminder text and date
    col1, col2 = st.columns([3, 1])
    with col1:
        reminder_text = st.text_input("Reminder", key="reminder_input")
    with col2:
        reminder_date = st.date_input("Date", value=datetime.date.today(), key="reminder_date")

    add_btn = st.button("Add Reminder")

    # Add the reminder on button click
    if add_btn:
        if reminder_text.strip():
            st.session_state.top_reminders.append({
                "reminder": reminder_text.strip(),
                "date": reminder_date
            })
            st.session_state.reminder_input = ""  # clear input
            st.success("Reminder added!")
        else:
            st.warning("Reminder cannot be empty.")

    # Display all reminders sorted by date ascending
    if st.session_state.top_reminders:
        st.markdown("---")
        st.subheader("All Top Reminders (sorted)")

        # Sort reminders by date
        reminders_sorted = sorted(
            enumerate(st.session_state.top_reminders),
            key=lambda x: x[1]["date"]
        )

        remove_indices = []
        for display_i, (orig_i, reminder) in enumerate(reminders_sorted):
            cols = st.columns([0.05, 0.95])
            with cols[0]:
                checked = st.checkbox("", key=f"topreminder_chk_{display_i}")
            with cols[1]:
                st.info(
                    f'📅 {reminder["date"].strftime("%a, %d %b %Y")}: {reminder["reminder"]}',
                    icon="⏰"
                )
            if checked:
                remove_indices.append(orig_i)

        # Remove reminders that were checked
        if remove_indices:
            # Remove duplicates & sort descending so pop does not affect indices
            for idx in sorted(set(remove_indices), reverse=True):
                st.session_state.top_reminders.pop(idx)
            st.success(f"Removed {len(remove_indices)} reminder(s).")
            st.experimental_rerun()
    else:
        st.info("No reminders yet!")
