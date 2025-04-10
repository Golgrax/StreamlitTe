import streamlit as st
from streamlit_extras.switch_page import switch_page
import requests
from datetime import datetime

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

st.title("Activity Logs")
response = requests.get("http://127.0.0.1:8000/api/get-logs/")
if response.status_code == 200:
    logs = response.json()
    today = datetime.now().date()
    filtered_logs = [f"{datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00')).strftime('%I:%M:%S %p')} - {log['behavior']}"
                     for log in logs if datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00')).date() == today]
    st.text("\n".join(filtered_logs))
else:
    st.error("Failed to fetch logs.")
