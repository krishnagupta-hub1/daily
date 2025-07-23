import streamlit as st
import datetime
from core.data_handler import save_data

def draw():
    st.title("📅 Important Dates")
    with st.form(key="important_dates_form"):
        topic = st.text_input("Enter important topic/description:")
        imp_date = st.date_input("Select date for topic:", value=datetime.date.today())
        submitted = st.form_submit_button("Add Important Date")
        if submitted and topic:
            st.session_state.important_dates.append({"topic": topic.strip(), "date": imp_date.isoformat()})
            st.session_state.important_dates = sorted(st.session_state.important_dates, key=lambda x: x["date"])
            save_data()
    st.markdown("### Saved Important Dates")
    for entry in st.session_state.important_dates:
        st.markdown(f"<div style='background:#F8F2FC;border-radius:8px;padding:7px;margin-bottom:4px;'><b>{entry['date']}</b>: {entry['topic']}</div>", unsafe_allow_html=True)
