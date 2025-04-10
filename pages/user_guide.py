import streamlit as st
from streamlit_extras.switch_page import switch_page

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

st.title("About Us" if "about_us" in __file__ else "Help" if "help" in __file__ else "User Guide" if "user_guide" in __file__ else "FAQs")
st.write("Content placeholder for this page.")
