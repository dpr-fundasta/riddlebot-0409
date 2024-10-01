import streamlit as st
from database.user_management import user_registration, login_check
from time import sleep
from navigation import make_sidebar
st.session_state.logged_in = False
st.session_state.username = ""
# Custom CSS for styling
st.markdown("""
    <style>
    .auth-container {
   
    }
    .signup_form header {
        text-align: center;
        margin-bottom: 20px;
    }
    .signup_form input {
        width: 100%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .signup_form button {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: none;
        background-color: #007bff;
        color: #fff;
        font-size: 16px;
        cursor: pointer;
    }
    .signup_form button:hover {
        background-color: #0056b3;
    }
    .auth-link {
        text-align: center;
        margin-top: 20px;
    }
    .auth-link a {
        color: #007bff;
        text-decoration: none;
    }
    .auth-link a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
make_sidebar()
# Title of the app
st.title("LLM RIDDLEBOT - FundastA")

# Sidebar for switching between Login and SignUp
menu = ["Login", "SignUp"]
choice = st.sidebar.selectbox("Menu", menu)
def handle_login():
    st.subheader("Login Section")

    with st.form(key='login_form', clear_on_submit=True):
        username = st.text_input("User Name", key='login_username')
        password = st.text_input("Password", type='password', key='login_password')
        submit_button = st.form_submit_button("Login")

        if submit_button:
            response = login_check(username, password)
            if response == "Login successful":
                if username == 'admin':
                    st.session_state.logged_in = True
                    st.session_state.username = "admin"
                    st.success(f"Logged In as {username}. Redirecting to admin page...")
                    sleep(0.5)
                    st.switch_page("pages/HOME.py")
                else:
                    st.session_state.logged_in = True
                    st.session_state.username = f"{username}"
                    st.success(f"Logged In as {username}")
                    sleep(0.5)
                    st.switch_page("pages/HOME.py")
            elif response == "Your account is pending approval by an admin.":
                st.info(response)
            elif response == "Your account has been rejected.":
                st.error(response)
            else:
                st.warning(response)
def handle_signup():
    st.subheader("Create New Account")

    with st.form(key='signup_form', clear_on_submit=True):
        new_user = st.text_input("Username", key='signup_username')
        new_password = st.text_input("Password", type='password', key='signup_password')
        submit_button = st.form_submit_button("Signup")

        if submit_button:
            response = user_registration(new_user, new_password)
            if response == "User registered successfully.":
                st.success(response)
                sleep(0.5)
                st.rerun()  # Optionally reload the page
            else:
                st.warning(response)

# Render the appropriate page based on the sidebar selection
if choice == "Login":
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        handle_login()
        st.markdown('</div>', unsafe_allow_html=True)
elif choice == "SignUp":
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        handle_signup()
        st.markdown('</div>', unsafe_allow_html=True)
