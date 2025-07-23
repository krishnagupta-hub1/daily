import streamlit as st
from core.data_handler import save_data

def draw():
    st.title("🔄 App Update")
    left_col, right_col = st.columns(2)
    with left_col:
        todays_update = st.text_input("", placeholder="Today's Update")
        if st.button("Submit Update") and todays_update:
            st.session_state.app_updates.append(todays_update)
            save_data()
        if st.button("Delete Last Update") and st.session_state.app_updates:
            st.session_state.app_updates.pop()
            save_data()
        for i, upd in enumerate(st.session_state.app_updates, 1):
            st.markdown(f"**{i}.** {upd}")
    with right_col:
        another_idea = st.text_input(" ", placeholder="Another Idea")
        if st.button("Submit Idea") and another_idea:
            st.session_state.app_ideas.append(another_idea)
            save_data()
        if st.button("Delete Last Idea") and st.session_state.app_ideas:
            st.session_state.app_ideas.pop()
            save_data()
        for i, idea in enumerate(st.session_state.app_ideas, 1):
            st.markdown(f"**{i}.** {idea}")
