import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# API base URL (replace with your actual backend URL)
API_URL = "https://api.example.com"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_data'] = {}
    st.session_state['token'] = None
    st.session_state['page'] = 'main'

# Helper function to fetch data from API
def fetch_from_api(endpoint, method='GET', data=None):
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    url = f"{API_URL}/{endpoint}"
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, json=data, headers=headers)
    elif method == 'PUT':
        response = requests.put(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

# Main page (MainScreen)
def show_main():
    st.image("assets/logo2.png", width=150)
    st.title("P E T W A T C H")
    st.markdown("Your pet's best friend!")
    if st.button("LOGIN"):
        st.session_state['page'] = 'login'
        st.rerun()
    if st.button("SIGN UP"):
        st.session_state['page'] = 'signup'
        st.rerun()

# Signup page (SignupScreen)
def show_signup():
    st.markdown("### Create an Account")
    st.markdown("Sign up to get started")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    show_password = st.checkbox("Show password")
    password = st.text_input("Password (at least 8 characters)", type="text" if show_password else "password")
    
    if st.button("SIGN UP"):
        if not all([first_name, last_name, email, password]):
            st.error("All fields are required.")
        elif len(password) < 8:
            st.error("Password must be at least 8 characters.")
        else:
            try:
                response = requests.post(f"{API_URL}/signup", json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password
                })
                response.raise_for_status()
                st.success("Signup successful! Please login.")
                st.session_state['page'] = 'login'
                st.rerun()
            except requests.RequestException as e:
                st.error(f"Signup failed: {e}")
    
    if st.button("Back to Login"):
        st.session_state['page'] = 'login'
        st.rerun()

# Login page (assumed, not provided in Kivy code)
def show_login():
    st.markdown("### Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("LOGIN"):
        try:
            response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
            response.raise_for_status()
            data = response.json()
            st.session_state['logged_in'] = True
            st.session_state['user_data'] = data['user']
            st.session_state['token'] = data['token']
            st.rerun()
        except requests.RequestException as e:
            st.error(f"Login failed: {e}")
    
    if st.button("Back to Main"):
        st.session_state['page'] = 'main'
        st.rerun()

# Dashboard (assumed as a landing page after login)
def show_dashboard():
    st.markdown("### Dashboard")
    st.write("Welcome to Petwatch! Here's an overview of your pet's status.")
    # Add dashboard content here (e.g., recent activity, pet status)

# Profile page (ProfileTabScreen/ProfileScreen)
def show_profile():
    st.markdown("### Profile")
    user = st.session_state['user_data']
    st.image("assets/profile_tab_removebg.png", width=170)
    st.write(f"Full Name: {user['first_name']} {user['last_name']}")
    st.write(f"Email: {user['email']}")
    if st.button("Edit Profile"):
        st.session_state['page'] = 'edit_profile'
        st.rerun()
    if st.button("Help"):
        st.session_state['page'] = 'user_guide'
        st.rerun()
    if st.button("About Us"):
        st.session_state['page'] = 'about_us'
        st.rerun()

# Edit Profile page (assumed from ProfileTabScreen button)
def show_edit_profile():
    st.markdown("### Edit Profile")
    user = st.session_state['user_data']
    first_name = st.text_input("First Name", value=user['first_name'])
    last_name = st.text_input("Last Name", value=user['last_name'])
    email = st.text_input("Email", value=user['email'])
    if st.button("Save"):
        try:
            data = {"first_name": first_name, "last_name": last_name, "email": email}
            fetch_from_api("user", method='PUT', data=data)
            st.session_state['user_data'].update(data)
            st.success("Profile updated successfully!")
            st.session_state['page'] = 'profile'
            st.rerun()
        except requests.RequestException as e:
            st.error(f"Failed to update profile: {e}")

# Pet Profile page (PetProfileScreen/PetTabScreen)
def show_pet_profile():
    st.markdown("### Pet Profile")
    try:
        pet = fetch_from_api("pet")
        st.write(f"Pet's Name: {pet['name']}")
        st.write(f"Breed: {pet['breed']}")
        st.write(f"Gender: {pet['gender']}")
        st.write(f"Age: {pet['age']} {pet['age_unit']}")
        if 'image' in pet and pet['image']:
            st.image(pet['image'])
        if st.button("Edit Pet Profile"):
            st.session_state['page'] = 'edit_pet_profile'
            st.rerun()
    except requests.RequestException as e:
        st.write("No pet profile found.")
        if st.button("Add Pet Profile"):
            st.session_state['page'] = 'edit_pet_profile'
            st.rerun()

# Edit Pet Profile page
def show_edit_pet_profile():
    st.markdown("### Edit Pet Profile")
    try:
        pet = fetch_from_api("pet")
    except requests.RequestException:
        pet = {}
    name = st.text_input("Pet's Name", value=pet.get('name', ''))
    breed = st.text_input("Breed", value=pet.get('breed', ''))
    gender = st.radio("Gender", ["Male", "Female"], index=0 if pet.get('gender') == "Male" else 1)
    age = st.number_input("Age", min_value=0, value=pet.get('age', 0))
    age_unit = st.selectbox("Age Unit", ["Years", "Months"], index=0 if pet.get('age_unit') == "Years" else 1)
    uploaded_file = st.file_uploader("Pet Image", type=["png", "jpg", "jpeg"])
    
    if st.button("Save"):
        try:
            data = {"name": name, "breed": breed, "gender": gender, "age": age, "age_unit": age_unit}
            if uploaded_file:
                # Handle image upload (assumes API accepts base64 or file upload)
                data['image'] = uploaded_file.read()  # Adjust based on API requirements
            fetch_from_api("pet", method='PUT' if pet else 'POST', data=data)
            st.success("Pet profile saved!")
            st.session_state['page'] = 'pet_profile'
            st.rerun()
        except requests.RequestException as e:
            st.error(f"Failed to save pet profile: {e}")

# Live Feed page (assumed from navigation)
def show_live_feed():
    st.markdown("### Live Feed")
    st_autorefresh(interval=100)  # Refresh every 100ms
    try:
        frame = fetch_from_api("live_feed")['frame']  # Assumes API returns image data
        st.image(frame, caption="Live Feed")
    except requests.RequestException as e:
        st.error(f"Failed to load live feed: {e}")

# Thermal Camera page (ThermalCameraScreen)
def show_thermal_camera():
    st.markdown("### Thermal Feed")
    st_autorefresh(interval=100)
    try:
        data = fetch_from_api("thermal_feed")
        st.image(data['frame'], caption="Thermal Feed")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Environment Temp: {data.get('env_temp', 'N/A')}")
        with col2:
            st.write(f"Dog Temp: {data.get('dog_temp', 'N/A')}")
    except requests.RequestException as e:
        st.error(f"Failed to load thermal feed: {e}")

# Activity Logs page (assumed from navigation)
def show_activity_logs():
    st.markdown("### Activity Logs")
    try:
        logs = fetch_from_api("activity_logs")
        st.table(logs)
    except requests.RequestException as e:
        st.error(f"Failed to load activity logs: {e}")

# User Guide page (UserGuideScreen)
def show_user_guide():
    st.markdown("### User Guide")
    st.markdown("""
    **Welcome to Petwatch!**

    Petwatch is a camera-based behavioral monitoring and mobile app designed to help you understand your pet's health and activities. Follow the guide below to get started.

    #### Step 1: Setting up the Camera
    - Position the camera in an area where your pet spends most of its time.
    - Ensure the camera is connected to power and a stable Wi-Fi network.
    - Link the camera to the Petwatch app by following the pairing instructions in the app's settings.

    #### Step 2: Monitoring your Pet
    - Open the app and navigate to the live camera feed to watch your pet in real-time.
    - Use the app to record behaviors, take snapshots, or review past recordings.

    #### Step 3: Viewing Behavioral Insights
    - Access the 'Insights' section to view detailed reports on your pet's behavior.
    - Review trends, alerts, and suggested actions based on AI analysis of your pet's activities.

    #### Need Help?
    - Check the FAQs section in the app for quick solutions.
    - Contact support via the app if you encounter any issues.
    """)

# About Us page (assumed from ProfileTabScreen button)
def show_about_us():
    st.markdown("### About Us")
    st.write("Petwatch is dedicated to helping pet owners keep their furry friends safe and healthy.")

# Main app logic
def main():
    if not st.session_state['logged_in']:
        if st.session_state['page'] == 'main':
            show_main()
        elif st.session_state['page'] == 'login':
            show_login()
        elif st.session_state['page'] == 'signup':
            show_signup()
    else:
        page = st.sidebar.selectbox(
            "Select Page",
            ["Dashboard", "Profile", "Pet Profile", "Live Feed", "Thermal Camera", "Activity Logs", "User Guide", "About Us", "Logout"]
        )
        if page == "Dashboard":
            show_dashboard()
        elif page == "Profile":
            show_profile()
        elif page == "Pet Profile":
            show_pet_profile()
        elif page == "Live Feed":
            show_live_feed()
        elif page == "Thermal Camera":
            show_thermal_camera()
        elif page == "Activity Logs":
            show_activity_logs()
        elif page == "User Guide":
            show_user_guide()
        elif page == "About Us":
            show_about_us()
        elif page == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['user_data'] = {}
            st.session_state['token'] = None
            st.session_state['page'] = 'main'
            st.rerun()

if __name__ == "__main__":
    main()
