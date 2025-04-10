# pages/pet_profile.py
import streamlit as st
import requests

def display_pet_profile():
    if not st.session_state['logged_in']:
        st.error("Please log in to access this page.")
        return

    st.title("Pet Profile")
    email = st.session_state['user_data'].get('email', '')
    pet_name = st.text_input("Pet's Name")
    pet_breed = st.text_input("Breed")
    gender = st.radio("Sex", ["Male", "Female"])
    pet_age = st.number_input("Age", min_value=0, step=1)
    age_unit = st.selectbox("Age Unit", ["Years", "Months"])

    if st.button("Save"):
        url = 'http://127.0.0.1:8000/pet_profile/'
        data = {
            'email': email,
            'pet_name': pet_name,
            'pet_breed': pet_breed,
            'pet_age': pet_age,
            'age_unit': age_unit,
            'gender': gender
        }
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                st.success("Pet profile saved successfully!")
            else:
                st.error("Failed to save pet profile.")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == '__main__':
    display_pet_profile()
