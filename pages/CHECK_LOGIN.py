import streamlit as st


def check_login():
    """
    Check if the user is logged in by verifying
    the existence of 'username' and 'logged_in'
    in session state. Redirects to login page if not.
    """
    if "username" not in st.session_state or "logged_in" not in st.session_state:
        st.session_state.username = None  # Initialize if not set
        st.session_state.logged_in = False  # Initialize if not set
        st.switch_page("login.py")  # Redirect to login page

    elif st.session_state.logged_in == False:
        st.switch_page("login.py")