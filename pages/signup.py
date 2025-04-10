import streamlit as st
from streamlit_extras.switch_page import switch_page
import requests

st.title("Signup")
if st.button("← Back"):
    switch_page("pages/login.py")

st.markdown("<h1 style='text-align: center; color: #4F3630;'>Create an Account</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #875012;'>Sign up to get started</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    first_name = st.text_input("First Name", placeholder="First Name")
with col2:
    last_name = st.text_input("Last Name", placeholder="Last Name")
email = st.text_input("Email", placeholder="Email")
password = st.text_input("Password", type="password", placeholder="Password (at least 8 characters)")

error_message = st.empty()
if st.button("SIGN UP"):
    full_name = f"{first_name} {last_name}"
    if not first_name or not last_name:
        error_message.error("Please enter both first and last names.")
    elif not email.endswith(('@yahoo.com', '@gmail.com')):
        error_message.error("Please use a @yahoo.com or @gmail.com email.")
    elif len(password) < 8:
        error_message.error("Password must be at least 8 characters long.")
    else:
        response = requests.post("http://127.0.0.1:8000/signup/", json={
            "first_name": first_name, "last_name": last_name, "email": email, "password": password
        })
        if response.status_code in [201, 226]:
            response = requests.post("http://127.0.0.1:8000/login/", json={"email": email, "password": password})
            if response.status_code == 200:
                st.session_state['logged_in'] = True
                st.session_state['user_data'] = response.json()
                switch_page("pages/profile.py")
        else:
            error_message.error(response.json().get('message', 'Signup failed'))

st.write("Already have an account?")
if st.button("Login"):
    switch_page("pages/login.py")
