# pages/signup.py
import streamlit as st
import requests

def display_signup():
    if st.session_state['logged_in']:
        st.write("You are already logged in.")
        return

    st.title("Sign Up")
    st.image("../assets/signup.png", use_column_width=True)
    st.markdown("<h2 style='color: #4F3630;'>Create an Account</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #875012;'>Sign up to get started</p>", unsafe_allow_html=True)

    first_name = st.text_input("First Name", placeholder="First Name")
    last_name = st.text_input("Last Name", placeholder="Last Name")
    email = st.text_input("Email", placeholder="Email")
    password = st.text_input("Password", type="password", placeholder="Password (at least 8 characters)")

    if st.button("Sign Up"):
        if len(password) < 8:
            st.error("Password must be at least 8 characters long.")
            return
        url = 'http://127.0.0.1:8000/signup/'
        data = {'first_name': first_name, 'last_name': last_name, 'email': email, 'password': password}
        try:
            response = requests.post(url, json=data)
            if response.status_code in [201, 226]:
                user_data = response.json()
                st.session_state['logged_in'] = True
                st.session_state['user_data'] = user_data
                st.session_state['page'] = 'dashboard'
                st.rerun()
            else:
                st.error(response.json().get('message', 'Signup failed'))
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Back to Login"):
        st.session_state['page'] = 'login'
        st.rerun()

if __name__ == '__main__':
    display_signup()
