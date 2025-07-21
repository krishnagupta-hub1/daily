import streamlit as st
from datetime import datetime
import pytz

# Set up Streamlit page
st.set_page_config(page_title="Daily Reminder App", layout="wide")

# Display current IST date and time
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).strftime("%H:%M:%S")
today = datetime.now(ist).strftime("%A, %d %B %Y")

st.markdown("<h1 style='text-align: center; color: white;'>📅 Daily Reminder App</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: white;'>🕒 {today} | Indian Standard Time: {current_time}</h3>", unsafe_allow_html=True)

# Sidebar navigation
page = st.sidebar.radio("Go to", ["Home", "Afternoon Schedule"])

# ---------------------- HOME PAGE ---------------------- #
if page == "Home":
    st.markdown("<h2 style='color:white;'>📝 Daily Checklist</h2>", unsafe_allow_html=True)

    # Morning Exercise
    st.markdown("""
    <div style='background-color:#f5f5f5;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>🏃‍♂️ Morning 30 min Exercise</h4>
        <label><input type='checkbox'> Pushups</label><br>
        <label><input type='checkbox'> Crunches</label><br>
        <label><input type='checkbox'> Bhujangasana</label><br>
        <label><input type='checkbox'> Side Planks / Russian Twist</label>
    </div>
    """, unsafe_allow_html=True)

    # Jawline Routine
    st.markdown("""
    <div style='background-color:#ffe6e6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>😁 Jawline Routine</h4>
        <label><input type='checkbox'> Stretching</label><br>
        <label><input type='checkbox'> Upward Chin</label><br>
        <label><input type='checkbox'> 2 Video Routine</label>
    </div>
    """, unsafe_allow_html=True)

    # Duolingo
    st.markdown("""
    <div style='background-color:#e6ffe6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>📘 DUOLINGO</h4>
        <label><input type='checkbox'> 100 - 150 XP completed</label>
    </div>
    """, unsafe_allow_html=True)

# ---------------------- AFTERNOON SCHEDULE ---------------------- #
elif page == "Afternoon Schedule":
    st.markdown("<h2 style='color:white;'>🌤️ Afternoon Schedule</h2>", unsafe_allow_html=True)

    # Morning Exercise - Light Grey
    st.markdown("""
    <div style='background-color:#f5f5f5;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>🏃‍♂️ Morning 30 min Exercise</h4>
        <ul>
            <li>Pushups 30</li>
            <li>Crunches 30</li>
            <li>Side planks or Russian twist 30</li>
            <li>Bhujangasana 30 sec</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Jawline Routine - Light Red
    st.markdown("""
    <div style='background-color:#ffe6e6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>😁 Jawline Routine</h4>
        <h5>1. Warm Up</h5>
        <ul>
            <li>Upward stretch</li>
            <li>Face upward rotate 180</li>
            <li>Stretching face both sides</li>
        </ul>
        <h5>2. Vid 1</h5>
        <p>[Video Placeholder for Vid 1]</p>
        <h5>3. Vid 2</h5>
        <p>[Video Placeholder for Vid 2]</p>
    </div>
    """, unsafe_allow_html=True)

    # Duolingo - Light Green
    st.markdown("""
    <div style='background-color:#e6ffe6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>📘 DUOLINGO</h4>
        <label><input type='checkbox'> 100 - 150 XP completed</label>
    </div>
    """, unsafe_allow_html=True)

    # Classroom Studies - Light Yellow
    st.markdown("""
    <div style='background-color:#fff9e6;color:#000000;padding:20px;border-radius:10px;margin-top:25px;'>
        <h4>🏫 Classroom Studies</h4>
        <ul>
            <li><strong>OS:</strong> Scheduling + Banker's Algo</li>
            <li><strong>DBMS:</strong> Keys + Normalisation + Transactions + Indexing</li>
            <li><strong>CN:</strong> Error + CRC + Flow control + Congestion control + IP addressing</li>
            <li><strong>TOC:</strong> CFG + PDA + Pumping Lemma</li>
            <li><strong>Compiler:</strong> Lexical + Syntax + Semantic + Intermediate</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
