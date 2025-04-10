# pages/dashboard.py
import streamlit as st
import requests

def display_dashboard():
    if not st.session_state['logged_in']:
        st.error("Please log in to access the dashboard.")
        return

    st.title("Dashboard")
    user_data = st.session_state['user_data']
    st.markdown(f"<h3>Hello, <b>{user_data.get('full_name', 'User')}</b></h3>", unsafe_allow_html=True)
    
    # Fetch pet profile
    email = user_data.get('email', '')
    url = f'http://127.0.0.1:8000/pet_profile/?email={email}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pet_profile = response.json()[0] if isinstance(response.json(), list) else response.json()
            st.write(f"Name: {pet_profile.get('pet_name', 'N/A')}")
            st.write(f"Breed: {pet_profile.get('breed', 'N/A')}")
            st.write(f"Age: {pet_profile.get('age', 'N/A')} {pet_profile.get('age_unit', '')} old")
            st.write(f"Gender: {pet_profile.get('gender', 'N/A')}")
    except Exception as e:
        st.write("No pet profile available.")

if __name__ == '__main__':
    display_dashboard()
