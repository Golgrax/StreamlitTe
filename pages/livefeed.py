# pages/live_feed.py
import streamlit as st
import cv2
import time

def display_live_feed():
    if not st.session_state['logged_in']:
        st.error("Please log in to access the live feed.")
        return

    st.title("Live Feed")
    if 'cap' not in st.session_state:
        st.session_state['cap'] = cv2.VideoCapture('rtsp://admin:L2A51CBA@192.168.0.102:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif')
    
    cap = st.session_state['cap']
    placeholder = st.empty()
    
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        placeholder.image(frame, channels="RGB")
    time.sleep(0.1)  # Update every 0.1 seconds
    st.rerun()

if __name__ == '__main__':
    display_live_feed()
