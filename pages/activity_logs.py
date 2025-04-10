# pages/activity_logs.py
import streamlit as st
import requests
from datetime import datetime

def display_activity_logs():
    if not st.session_state['logged_in']:
        st.error("Please log in to access activity logs.")
        return

    st.title("Activity Logs")
    st.write(datetime.now().strftime("%A, %B %d, %Y"))
    
    response = requests.get('http://127.0.0.1:8000/api/get-logs/')
    if response.status_code == 200:
        logs = response.json()
        for log in logs:
            st.write(f"{log['timestamp']} - {log['behavior']}")
    else:
        st.error("Failed to fetch logs.")

if __name__ == '__main__':
    display_activity_logs()
