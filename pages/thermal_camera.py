import streamlit as st
from streamlit_autorefresh import st_autorefresh
import numpy as np
import cv2
import requests
import matplotlib.pyplot as plt
from streamlit_extras.switch_page import switch_page

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

def fetch_thermal_data():
    response = requests.get("http://192.168.0.200/thermal")
    if response.status_code == 200:
        return [float(i) for i in response.text.split(',')]
    return None

st_autorefresh(interval=1000)
data = fetch_thermal_data()
if data:
    data_matrix = np.array(data).reshape(24, 32)
    smoothed_data = cv2.GaussianBlur(data_matrix, (3, 3), 0)
    resized_data = cv2.resize(smoothed_data, (320, 240), interpolation=cv2.INTER_LANCZOS4)
    normalized_data = cv2.normalize(resized_data, None, 0, 1, cv2.NORM_MINMAX)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(normalized_data, cmap='inferno')
    plt.axis('off')
    st.pyplot(plt)
    
    env_temp = np.mean(data_matrix)
    st.write(f"Environment Temperature: {env_temp:.2f}°C")
else:
    st.write("Failed to fetch thermal data.")
