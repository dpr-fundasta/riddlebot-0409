import streamlit as st
from navigation import make_sidebar, admin_make_sidebar

if st.session_state.username == "admin":
    admin_make_sidebar()
else:
    make_sidebar()


st.markdown(
    """
    <style>
    body {
        background-image: url("");
        background-size: cover;
        color: #FFFFFF;
    }
    .stTextInput>div>input {
        background-color: #333333;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50; /* Button background color */
        color: white; /* Text color */
        font-size: 16px; /* Font size */
        padding: 10px 20px; /* Padding inside the button */
        border-radius: 8px; /* Rounded corners */
        border: none; /* Remove border */
        cursor: pointer; /* Change cursor to pointer on hover */
        width: 110px; /* Width of the button */
        height: 40px; /* Height of the button */
        margin-top: 27px; /* Adjust this value to move the button down */
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .button-container {
        display: flex;
        justify-content: flex-start;
        gap: 10px;
    }

    .title {
        font-size: 30px; 
        color: #333333; 
        text-align: center; 
        margin:20px;
        padding:20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

score_style = """
    <style>
     .score-debug {
        font-size: 15px;
        font-weight: bold;
        color: #2c3e50;
    }
    </style>
"""

st.markdown("<div class='score-debug'>DEBUG TERMINAL：</div>", unsafe_allow_html=True)
st.write("Database")
st.write(st.session_state.riddle_data)
st.write("Reasoning of the judgement")
st.write(st.session_state.reasoning)
st.write("History")
st.write(st.session_state.hint_history)
st.write("Username")
st.write(st.session_state.username)


if st.session_state.error != "":
    st.write("Error Message")
    st.write(st.session_state.error)
