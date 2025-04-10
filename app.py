import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Apply background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("assets/image.png");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Center content using columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("assets/logo2.png", width=150)
    st.markdown("<h1 style='text-align: center; color: #4F3630;'>P E T W A T C H</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #875012;'>Your pet's best friend!</p>", unsafe_allow_html=True)
    
    if st.button("LOGIN"):
        switch_page("pages/login.py")
    if st.button("SIGN UP"):
        switch_page("pages/signup.py")
