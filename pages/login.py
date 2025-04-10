# pages/login.py
import streamlit as st
import requests

def display_login():
    if st.session_state['logged_in']:
        st.write("You are already logged in.")
        return

    st.title("Login")
    st.image("../assets/login.png", use_column_width=True)
    st.markdown("<h2 style='color: #4F3630;'>Welcome!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #875012;'>Sign in to continue</p>", unsafe_allow_html=True)

    email = st.text_input("Email", placeholder="Email")
    password = st.text_input("Password", type="password", placeholder="Password")
    
    if st.button("Login"):
        url = 'http://127.0.0.1:8000/login/'
        data = {'email': email, 'password': password}
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                user_data = response.json()
                st.session_state['logged_in'] = True
                st.session_state['user_data'] = user_data
                st.session_state['page'] = 'dashboard'
                st.rerun()
            else:
                st.error(response.json().get('error', 'Login failed'))
        except Exception as e:
            st.error(f"Error: {e}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Forgot Password"):
            st.session_state['page'] = 'forgot_password'
            st.rerun()
    with col2:
        if st.button("Sign Up"):
            st.session_state['page'] = 'signup'
            st.rerun()

if __name__ == '__main__':
    display_login()
