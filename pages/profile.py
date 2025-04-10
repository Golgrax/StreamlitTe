import streamlit as st
from streamlit_extras.switch_page import switch_page

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

user_data = st.session_state['user_data']
st.image("assets/profile_tab_removebg.png", width=300)
st.markdown(f"<h2>First Name: {user_data['first_name']}</h2>", unsafe_allow_html=True)
st.markdown(f"<h2>Last Name: {user_data['last_name']}</h2>", unsafe_allow_html=True)
st.markdown(f"<h2>Email: {user_data['email']}</h2>", unsafe_allow_html=True)

if st.button("Next"):
    switch_page("pages/pet_profile.py")
