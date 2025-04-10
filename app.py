# app.py
import streamlit as st

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_data'] = {}
    st.session_state['page'] = 'main'

def show_main():
    st.title("Welcome to PetWatch")
    st.image("assets/image.png", use_column_width=True)
    st.image("assets/logo2.png", width=150)
    st.markdown("<h1 style='text-align: center; color: #4F3630;'>P E T W A T C H</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #875012;'>Your pet's best friend!</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state['page'] = 'login'
            st.rerun()
    with col2:
        if st.button("Sign Up"):
            st.session_state['page'] = 'signup'
            st.rerun()

def main():
    if not st.session_state['logged_in']:
        if st.session_state['page'] == 'main':
            show_main()
        # Other pages like login and signup will be handled in their respective files
    else:
        # Sidebar navigation for logged-in users
        page = st.sidebar.selectbox(
            'Select Page',
            ['Dashboard', 'Profile', 'Pet Profile', 'Live Feed', 'Thermal Camera', 'Activity Logs', 'Logout']
        )
        st.session_state['page'] = page.lower().replace(' ', '_')
        if page == 'Logout':
            st.session_state['logged_in'] = False
            st.session_state['user_data'] = {}
            st.session_state['page'] = 'main'
            st.rerun()

if __name__ == '__main__':
    main()
