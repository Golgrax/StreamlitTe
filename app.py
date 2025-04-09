import streamlit as st

# Initialize session state for authentication
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_data'] = {}
    st.session_state['page'] = 'main'

def main():
    if not st.session_state['logged_in']:
        if st.session_state['page'] == 'main':
            show_main()
        elif st.session_state['page'] == 'login':
            show_login()
        elif st.session_state['page'] == 'signup':
            show_signup()
    else:
        # Sidebar navigation for logged-in users
        page = st.sidebar.selectbox('Select Page', ['Dashboard', 'Profile', 'Pet Profile', 'Live Feed', 'Thermal Camera', 'Activity Logs', 'Logout'])
        if page == 'Dashboard':
            show_dashboard()
        elif page == 'Profile':
            show_profile()
        elif page == 'Pet Profile':
            show_pet_profile()
        elif page == 'Live Feed':
            show_live_feed()
        elif page == 'Thermal Camera':
            show_thermal_camera()
        elif page == 'Activity Logs':
            show_activity_logs()
        elif page == 'Logout':
            st.session_state['logged_in'] = False
            st.session_state['user_data'] = {}
            st.session_state['page'] = 'main'
            st.rerun()

if __name__ == '__main__':
    main()
