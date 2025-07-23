import os
import json
import streamlit as st

# Default structure to use when data.json is not created yet
DEFAULT_DATA = {
    "classroom_tasks": {
        "Database System": [],
        "Operating Systems": [],
        "Compiler Design": [],
        "Computer Networks": [],
        "Cloud Architecture Design": [],
    },
    "completed_classroom_tasks": {
        "Database System": {},
        "Operating Systems": {},
        "Compiler Design": {},
        "Computer Networks": {},
        "Cloud Architecture Design": {},
    },
    "app_updates": [],
    "app_ideas": [],
    "duolingo_records": {},
    "morning_exercise_records": {},
    "jawline_records": {},
    "dairy_records": {},
    "water_counts": {},
    "water_checklists": {},
    "water_main_checklist": {},
    "passwords": {
        "Folder 1": [],
        "Folder 2": [],
        "Folder 3": [],
        "Folder 4": [],
    },
    "dsa_sheet": [{} for _ in range(18)],
    "important_dates": []
}

def load_data():
    """Load data.json or return default if not found"""
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data():
    """Save session_state into data.json safely"""
    with open("data.json", "w") as f:
        json.dump({
            "classroom_tasks": st.session_state.classroom_tasks,
            "completed_classroom_tasks": st.session_state.completed_classroom_tasks,
            "app_updates": st.session_state.app_updates,
            "app_ideas": st.session_state.app_ideas,
            "duolingo_records": st.session_state.duolingo_records,
            "morning_exercise_records": st.session_state.morning_exercise_records,
            "jawline_records": st.session_state.jawline_records,
            "dairy_records": st.session_state.dairy_records,
            "water_counts": st.session_state.water_counts,
            "water_checklists": st.session_state.water_checklists,
            "water_main_checklist": st.session_state.water_main_checklist,
            "passwords": st.session_state.passwords,
            "dsa_sheet": st.session_state.dsa_sheet,
            "important_dates": st.session_state.important_dates,
        }, f)
