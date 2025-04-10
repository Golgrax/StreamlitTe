import streamlit as st
from streamlit_extras.switch_page import switch_page
import requests

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

st.title("Pet Profile")
st.image("assets/add_image.png", width=100)
email = st.session_state['user_data']['email']
st.text_input("Email", value=email, disabled=True)
pet_name = st.text_input("Pet's Name")
breed = st.text_input("Breed")
gender = st.radio("Sex", ["Male", "Female"])
age = st.number_input("Age", min_value=0, step=1)
age_unit = st.selectbox("Age Unit", ["Years", "Months"])

if st.button("Save"):
    if not all([pet_name, breed, age, gender, age_unit]):
        st.error("Please fill in all fields.")
    else:
        response = requests.post("http://127.0.0.1:8000/pet_profile/", json={
            "email": email, "pet_name": pet_name, "pet_breed": breed, "pet_age": age,
            "age_unit": age_unit, "gender": gender
        })
        if response.status_code == 201:
            switch_page("pages/dashboard.py")
        else:
            st.error("Failed to save pet profile.")

if st.button("Back"):
    switch_page("pages/profile.py")
