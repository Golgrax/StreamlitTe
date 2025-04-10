import streamlit as st
from streamlit_extras.switch_page import switch_page
import requests

if not st.session_state.get('logged_in', False):
    switch_page("pages/login.py")

st.title("Edit Pet Profile")
email = st.session_state['user_data']['email']
response = requests.get(f"http://127.0.0.1:8000/pet_profile/?email={email}")
pet = response.json()[0] if response.status_code == 200 and response.json() else {}

pet_name = st.text_input("Pet's Name", value=pet.get('pet_name', ''))
new_pet_name = st.text_input("New Pet's Name", value=pet.get('pet_name', ''))
breed = st.text_input("Breed", value=pet.get('breed', ''))
gender = st.radio("Sex", ["Male", "Female"], index=0 if pet.get('gender', '') == "Male" else 1)
age = st.number_input("Age", min_value=0, value=pet.get('age', 0))
age_unit = st.selectbox("Age Unit", ["Years", "Months"], index=0 if pet.get('age_unit', '') == "Years" else 1)

if st.button("Save Changes"):
    response = requests.put("http://127.0.0.1:8000/update_pet_profile/", json={
        "pet_name": pet_name, "new_pet_name": new_pet_name, "pet_breed": breed,
        "pet_age": age, "gender": gender, "age_unit": age_unit
    })
    if response.status_code == 200:
        st.success("Pet profile updated!")
        switch_page("pages/dashboard.py")
    else:
        st.error("Failed to update pet profile.")
