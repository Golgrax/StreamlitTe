import streamlit as st
# from streamlit_extras.switch_page import switch_page
import requests

# Redirect if already logged in
if st.session_state.get('logged_in', False):
    switch_page("pages/dashboard.py")

st.title("Login")
if st.button("← Back"):
    switch_page("app.py")

st.markdown("<h1 style='text-align: center; color: #4F3630;'>W e l c o m e!</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #875012;'>Sign in to continue</p>", unsafe_allow_html=True)

email = st.text_input("Email", placeholder="Email")
password = st.text_input("Password", type="password", placeholder="Password")

if st.button("LOGIN"):
    if not email or not password:
        st.error("Please enter both email and password.")
    else:
        response = requests.post("http://127.0.0.1:8000/login/", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state['logged_in'] = True
            st.session_state['user_data'] = response.json()
            switch_page("pages/dashboard.py")
        else:
            st.error(response.json().get('error', 'Login failed'))

if st.button("Forgot Password?"):
    switch_page("pages/forgot_password.py")

if st.button("Don't have an account? Sign up"):
    switch_page("pages/signup.py")
