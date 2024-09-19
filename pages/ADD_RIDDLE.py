import streamlit as st
st.set_page_config(page_title=" 新しい謎を追加", page_icon="📝")
from database.riddleFetch import  add_riddle

# Sidebar: Add a new riddle
from navigation import make_sidebar, admin_make_sidebar
if st.session_state.username=="admin":
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


st.title("📝 新しい謎を追加")
with st.form(key='riddle_form', clear_on_submit=True, border= True):
    question_input = st.text_input("謎の質問", st.session_state.get("question_input", ""))
    answer_input = st.text_input("正解の答え", st.session_state.get("answer_input", ""))
   
    submit_button = st.form_submit_button(label="謎を追加")

if submit_button:
    if question_input and answer_input:
        
        add_riddle(question_input, answer_input)
        st.toast("✅ 謎が正常に追加されました！")
        #st.sidebar.success("Riddle added successfully!")
        
        # Clear the sidebar text inputs
        st.session_state["question_input"] = ""
        st.session_state["answer_input"] = ""
        
    else:
        #st.sidebar.error("Please fill out the required fields!")
        st.toast(" ⚠️ 必須項目をすべて入力してください！")