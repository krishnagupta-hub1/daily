import streamlit as st
from core.date_utils import get_display_date

def draw():
    st.title("🏠 Welcome to Your Daily App")
    for i in range(1, 7):
        st.markdown(f"<div style='background-color:#d0ebff;padding:15px;border-radius:10px;margin-top:10px;'>🔹 Section {i}</div>", unsafe_allow_html=True)
    st.markdown("""<hr style='margin-top:30px;margin-bottom:10px;border:1px solid #ccc;'>""", unsafe_allow_html=True)
    st.markdown("""
        <div style='font-size:16px;color:#888;'>
            <strong>#At Night</strong><br>
            Update dairy / Twitter / Git<br>
            Check mails / LinkedIn / Organisation / Instagram<br>
            (search / commitChanges)<br>
            - &nbsp;&nbsp;&nbsp; - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; -
        </div>
    """, unsafe_allow_html=True)
