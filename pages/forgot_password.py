import streamlit as st
from streamlit_extras.switch_page import switch_page
import requests

st.title("Forgot Password")
email = st.text_input("Email")
new_password = st.text_input("New Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Reset Password"):
    if new_password != confirm_password:
        st.error("Passwords do not match.")
    elif len(new_password) < 8:
        st.error("Password must be at least 8 characters long.")
    elif not email.endswith(('@gmail.com', '@yahoo.com')):
        st.error("Email must be a @gmail.com or @yahoo.com address.")
    else:
        response = requests.post("http://127.0.0.1:8000/forgot_password/", json={
            "email": email, "new_password": new_password, "confirm_password": confirm_password
        })
        if response.status_code == 200:
            st.success("Password reset successful!")
            switch_page("pages/login.py")
        else:
            st.error("Password reset failed.")
