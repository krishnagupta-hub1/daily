import streamlit as st
from core.data_handler import save_data

def draw():
    st.title("🔒 Password Vault")
    folders = ["Folder 1", "Folder 2", "Folder 3", "Folder 4"]
    with st.form(key="passwords_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        content = st.text_input("Content/Description")
        dest_folder = st.selectbox("Push to folder:", options=folders)
        submitted = st.form_submit_button("Push to Folder (Green Button)")
        if submitted and username and password and content and dest_folder:
            st.session_state.passwords[dest_folder].append({
                "username": username,
                "password": password,
                "content": content
            })
            save_data()
            st.success(f"Saved to {dest_folder}.")
    pw_cols = st.columns(4)
    for idx, folder in enumerate(folders):
        with pw_cols[idx]:
            st.markdown(f"<div style='background:#EDF4FF;border-radius:8px;padding:7px;text-align:center;font-weight:bold;'>{folder}</div>", unsafe_allow_html=True)
            for entry in st.session_state.passwords[folder]:
                st.markdown(f"<div style='background:#E8ECF1;border-radius:8px;padding:7px;margin:6px 0 6px 0;'>"
                            f"Content: {entry['content']}<br>Username: {entry['username']}<br>Password: {entry['password']}</div>", unsafe_allow_html=True)
