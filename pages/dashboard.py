import streamlit as st
from streamlit_extras.switch_page import switch_page
import requests

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

user_data = st.session_state['user_data']
full_name = user_data['full_name']
email = user_data['email']

st.markdown(f"<h1>Hello, {full_name}</h1>", unsafe_allow_html=True)
response = requests.get(f"http://127.0.0.1:8000/pet_profile/?email={email}")
if response.status_code == 200 and response.json():
    pet = response.json()[0]
    st.write(f"Pet Name: {pet['pet_name']}")
    st.write(f"Breed: {pet['breed']}")
    st.write(f"Age: {pet['age']} {pet['age_unit']} old")
    st.write(f"Gender: {pet['gender']}")
else:
    st.write("No pet profile available.")

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Live Feed"):
        switch_page("pages/live_feed.py")
with col2:
    if st.button("Activity Logs"):
        switch_page("pages/activity_logs.py")
with col3:
    if st.button("Profile"):
        switch_page("pages/profile_tab.py")
