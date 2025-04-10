import streamlit as st
from streamlit_extras.switch_page import switch_page

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

st.title("Profile")
user_data = st.session_state['user_data']
st.image("assets/profile_tab_removebg.png", width=300)
st.markdown(f"<h2>{user_data['full_name']}</h2>", unsafe_allow_html=True)
st.markdown(f"<h3>{user_data['email']}</h3>", unsafe_allow_html=True)

if st.button("Edit Profile"):
    switch_page("pages/edit_profile.py")
if st.button("Help"):
    switch_page("pages/help.py")
if st.button("About Us"):
    switch_page("pages/about_us.py")
if st.button("Log Out"):
    st.session_state['logged_in'] = False
    st.session_state.pop('user_data', None)
    switch_page("pages/login.py")
