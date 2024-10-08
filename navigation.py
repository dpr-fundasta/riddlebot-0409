import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def admin_make_sidebar():
    with st.sidebar:
        


        if st.session_state.get("logged_in", True):
            st.page_link("pages/ADD_RIDDLE.py", label="ADD RIDDLE", icon="📝")
            st.page_link("pages/DEBUG.py", label="DEBUG", icon="⚙️")
            st.page_link("pages/HOME.py", label="RIDDLE BOT", icon="🏠")
            st.page_link("pages/ADMIN.py", label="ACCOUNT REQUESTS", icon="➕")
            st.page_link("pages/EXPORT.py", label="HISTORY", icon="📤")
            st.page_link("pages/DB_MANAGEMENT.py", label="FILE UPLOAD", icon="📀")
            

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "login":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("login.py")

def make_sidebar():
    with st.sidebar:
    
        if st.session_state.get("logged_in", True):
            st.page_link("pages/ADD_RIDDLE.py", label="ADD RIDDLE", icon="📝")
            st.page_link("pages/DEBUG.py", label="DEBUG", icon="⚙️")
            st.page_link("pages/HOME.py", label="HOME", icon="🏠")
            st.page_link("pages/EXPORT.py", label="HISTORY", icon="📤")
        

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "login":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("login.py")


def logout():
    st.session_state.logged_in = False
    st.session_state.username= ""
    st.session_state.acount = 0
    st.session_state.qcount = 0
    st.session_state.error = ""
    if 'riddle_data' in st.session_state:
        del st.session_state['riddle_data']
    if 'reasoning' in st.session_state:
        del st.session_state['reasoning']
    if 'hint_history' in st.session_state:
        del st.session_state['hint_history']
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("login.py")