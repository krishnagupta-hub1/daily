import streamlit as st
from core.date_utils import get_today_date
from core.data_handler import save_data

def draw():
    st.title("📖 Dairy Entry")
    today_date = get_today_date()
    old_val = st.session_state.dairy_records.get(today_date, "")
    new_val = st.text_area("Your Dairy for Today:", value=old_val, height=350)
    if st.button("Save Dairy Entry"):
        st.session_state.dairy_records[today_date] = new_val
        save_data()
        st.success("Your dairy entry has been saved!")
