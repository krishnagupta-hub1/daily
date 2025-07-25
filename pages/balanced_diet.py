import streamlit as st

def draw():
    st.title("🥗 Balanced Diet")
    st.write("Log your meals and nutrition here.")

    # --- Setup
    meal_types = ["Breakfast", "Lunch", "Dinner"]
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Session state prep for plans, edit mode, and exceptions
    for meal in meal_types:
        val_key = f"{meal.lower()}_val"
        edit_key = f"{meal.lower()}_edit"
        excpt_key = f"{meal.lower()}_excpt"
        if val_key not in st.session_state:
            st.session_state[val_key] = ""
        if edit_key not in st.session_state:
            st.session_state[edit_key] = False
        if excpt_key not in st.session_state:
            st.session_state[excpt_key] = []   # List of {'day':..., 'exception':...}

    # --------- Display meal sections ---------
    for meal in meal_types:
        st.markdown(
            "<div style='background:#f8fafc;padding:25px 25px 10px 25px;border-radius:15px;margin-bottom:32px;'>",
            unsafe_allow_html=True,
        )
        st.subheader(meal)
        val_key = f"{meal.lower()}_val"
        edit_key = f"{meal.lower()}_edit"
        excpt_key = f"{meal.lower()}_excpt"

        # Edit mode for meal plan
        if st.session_state[edit_key]:
            new_val = st.text_area(
                f"Enter your {meal} plan:",
                value=st.session_state[val_key],
                key=f"{meal.lower()}_input",
                height=100,
            )
            save_btn = st.button(f"💾 Save {meal}", key=f"save_{meal.lower()}")
            cancel_btn = st.button("❌ Cancel", key=f"cancel_{meal.lower()}")
            if save_btn:
                st.session_state[val_key] = new_val.strip()
                st.session_state[edit_key] = False
                st.success(f"{meal} saved!")
                st.experimental_rerun()
            if cancel_btn:
                st.session_state[edit_key] = False
                st.experimental_rerun()
        # Display mode
        else:
            current_val = st.session_state[val_key]
            if current_val:
                st.success(f"{meal}: {current_val}")
            else:
                st.info(f"No {meal} logged yet.")

            edit_btn = st.button(f"✏️ Edit {meal}", key=f"edit_{meal.lower()}")
            if edit_btn:
                st.session_state[edit_key] = True
                st.experimental_rerun()

        # Show exceptions for this meal
        exceptions = st.session_state[excpt_key]
        if exceptions:
            st.markdown("**Exceptions (by day):**")
            for i, entry in enumerate(exceptions):
                with st.container():
                    st.info(f"**{entry['day']}**: {entry['exception']}", icon="💡")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Combined Exception Input Bar (for any meal) ----
    st.markdown("---")
    st.markdown("<h4>Add a Meal Exception For Any Day/Meal</h4>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2.5, 1.3, 1.3, 1.1])
    with col1:
        exception_input = st.text_input("Exception (food, activity, etc)", key="exception_input_new")
    with col2:
        day_choice = st.selectbox("Day", days_of_week, key="exception_day_new")
    with col3:
        meal_choice = st.selectbox("Meal", meal_types, key="exception_meal_new")
    with col4:
        save_excpt = st.button("Add Exception", key="add_exception_btn")

    # Save exception logic
    if save_excpt and exception_input.strip():
        # Avoid duplicate for same meal/day/exception if needed, or allow
        excpt_key = f"{meal_choice.lower()}_excpt"
        st.session_state[excpt_key].append({
            "day": day_choice,
            "exception": exception_input.strip()
        })
        st.success(f"Exception added for {meal_choice} on {day_choice}: {exception_input.strip()}")
        # Clear the input only
        st.session_state.exception_input_new = ""
        st.experimental_rerun()
    elif save_excpt:
        st.warning("Exception cannot be empty.")


