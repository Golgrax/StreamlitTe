import streamlit as st

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
