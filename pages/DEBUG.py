import streamlit as st

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
