# pages/thermal_camera.py
import streamlit as st
import requests
import numpy as np
import cv2
import time

def display_thermal_camera():
    if not st.session_state['logged_in']:
        st.error("Please log in to access the thermal camera.")
        return

    st.title("Thermal Camera")
    placeholder = st.empty()
    
    # Fetch thermal data
    response = requests.get('http://192.168.0.200/thermal')
    if response.status_code == 200:
        frame_data = [float(i) for i in response.text.split(',')]
        data_matrix = np.array(frame_data).reshape((24, 32))
        resized_data = cv2.resize(data_matrix, (320, 240), interpolation=cv2.INTER_LANCZOS4)
        normalized_data = cv2.normalize(resized_data, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        heatmap = cv2.applyColorMap(normalized_data, cv2.COLORMAP_INFERNO)
        placeholder.image(heatmap, channels="BGR")
    
    time.sleep(1)  # Update every second
    st.rerun()

if __name__ == '__main__':
    display_thermal_camera()
