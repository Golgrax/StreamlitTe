import streamlit as st
from streamlit_extras.switch_page import switch_page
import requests

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

st.title("Edit Profile")
user_data = st.session_state['user_data']
first_name = st.text_input("First Name", value=user_data['first_name'])
last_name = st.text_input("Last Name", value=user_data['last_name'])
email = st.text_input("Email", value=user_data['email'])

if st.button("Save Changes"):
    if not email.endswith(('@yahoo.com', '@gmail.com')):
        st.error("Please use a @yahoo.com or @gmail.com email.")
    else:
        response = requests.put("http://127.0.0.1:8000/update_profile/", json={
            "current_email": user_data['email'], "new_first_name": first_name,
            "new_last_name": last_name, "new_email": email
        })
        if response.status_code == 200:
            st.session_state['user_data'].update({"first_name": first_name, "last_name": last_name, "email": email, "full_name": f"{first_name} {last_name}"})
            st.success("Profile updated successfully!")
            switch_page("pages/profile_tab.py")
        else:
            st.error("Failed to update profile.")

if st.button("Cancel"):
    switch_page("pages/profile_tab.py")
