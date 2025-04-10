# pages/profile.py
import streamlit as st

def display_profile():
    if not st.session_state['logged_in']:
        st.error("Please log in to access your profile.")
        return

    st.title("Profile")
    user_data = st.session_state['user_data']
    st.write(f"First Name: {user_data.get('first_name', 'N/A')}")
    st.write(f"Last Name: {user_data.get('last_name', 'N/A')}")
    st.write(f"Email: {user_data.get('email', 'N/A')}")

if __name__ == '__main__':
    display_profile()
