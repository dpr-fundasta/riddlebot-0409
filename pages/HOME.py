import streamlit as st
from navigation import make_sidebar, admin_make_sidebar
# from streamlit_chat import message
from database.riddleFetch import fetch_random_riddle  # , add_riddle
from llm.definition import (
    judge_gemini_chain,
    judge_openai_chain,
    hint_gemini_chain,
    hint_openai_chain,
)
from llm.promptTemplates import (
    answer_checking_prompt_openai,
    answer_checking_prompt_gemini,
    hint_generation_prompt_openai,
    hint_generation_prompt_gemini,
)

from database.chat_history import add_data
from pages.CHECK_LOGIN import check_login
check_login()
st.set_page_config(page_title="謎解きゲームチャットボット", page_icon="🧩")


# Initialize the session state
def initialize_session_state():

    
    if "qcount" not in st.session_state:
        st.session_state.qcount = 0
    if "acount" not in st.session_state:
        st.session_state.acount = 0
    if "riddle_data" not in st.session_state:
        st.session_state.riddle_data = fetch_random_riddle()
    if "hint_history" not in st.session_state:
        st.session_state.hint_history = []
    if "text_input" not in st.session_state:  # my code
        st.session_state.text_input = ""
    if "reasoning" not in st.session_state:  # my code
        st.session_state.reasoning = ""
    if "error" not in st.session_state:  # my code
        st.session_state.error = ""


# Initialize session state on first load
initialize_session_state()


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
    unsafe_allow_html=True,
)


# Display the riddle
def display_riddle():
    riddle = st.session_state.riddle_data
    st.info(riddle["question"], icon="ℹ️")


st.markdown(
    '<h1 class="title">🤖 謎解きチャットボットへようこそ！</h1>', unsafe_allow_html=True
)

st.sidebar.markdown("<h3>🧠 LLMモデルを選択してください</h3>", unsafe_allow_html=True)
model = st.sidebar.radio("モデルを選択してください", ("ChatGPT", "Gemini"))

display_riddle()


def reload_riddle():
    st.session_state.riddle_data = fetch_random_riddle()
    st.session_state.reasoning = ""
    st.session_state.hint_history = []
    st.session_state.error = ""


with st.form(key="user_resp", border=False, clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        user_answer = st.text_input(
            "あなた： ", "", placeholder="ここに入力してください...!"
        )

    with col2:
        send_button = st.form_submit_button(label="送信")

    with col3:
        next_riddle = st.form_submit_button(label="次の謎")

if next_riddle:
    reload_riddle()
    st.rerun()

# Handle user input
if send_button and user_answer:
    # Add user input to chat history

    st.session_state.riddle_data["user_answer"] = user_answer
    if len(user_answer.strip()) > 0:
    # Choose the LLM model
        if model == "ChatGPT":
            response = judge_openai_chain(
                answer_checking_prompt_openai, st.session_state.riddle_data
            )
        else:
            try:
                response = judge_gemini_chain(
                    answer_checking_prompt_gemini, st.session_state.riddle_data
                )
            except Exception as e:
                 response = {
                "result":"Incorrect",
                "reasoning":"LLMはこのなぞなぞの結果と推論を生成することができなかった。H160"
                }
    else:
             response = {
                "result":"Incorrect",
                "reasoning":"ユーザーの答は空欄です。ユーザーは問題の意図を理解することが出来ず、何も答えることが出来ませんでした。そのためこの答えは間違ってます"
                }
       
    hint = ""
    if isinstance(response, dict) and "result" in response and "reasoning" in response:
        result = response["result"]
        reasoning = response["reasoning"]
    else:
   
        result = "Incorrect"
        reasoning = "LLMはこのなぞなぞの結果と推論を生成することができなかった。H170"
   
    st.session_state.reasoning = reasoning
    turn = min(len(st.session_state.hint_history), 2)

    if result.lower() == "correct":
        st.session_state.acount += 1
        st.success("正解です！", icon="✅")
        st.success("もう一度挑戦するには「次の謎」を押してください！")
        st.balloons()

    else:
        st.error("❌ 不正解です。ヒントをお教えします。")
        if model == "ChatGPT":
            hint = hint_openai_chain(
                hint_generation_prompt_openai,
                st.session_state.riddle_data,
                st.session_state.hint_history,
                turn,
                reasoning,
            )
        else:
            hint = hint_gemini_chain(
                hint_generation_prompt_gemini,
                st.session_state.riddle_data,
                st.session_state.hint_history,
                turn,
                reasoning,
            )

        st.session_state.hint_history.append(hint)

        st.error(hint)
        
    add_data(
        username = str(st.session_state.username),
        model = str(model),
        question = str(st.session_state.riddle_data["question"]),
        correct_answer = str(st.session_state.riddle_data["correct_answer"]),
        user_answer = str(user_answer),
        llm_response = str(result),
        reasoning =  str(reasoning),
        llm_hint = str(hint)
         )
    
    # Clear the text input box after submission
    st.session_state["text_input"] = ""

a_count = st.session_state.acount
q_count = st.session_state.qcount

# Define styles
score_style = """
    <style>
    .score-label {
        font-size: 23px;
        font-weight: bold;
        color: #2c3e50;
    }
    .score-value {
        font-size: 23px;
        font-weight: bold;
        color: #e74c3c;
    }
    </style>
"""

# Inject styles into the sidebar
st.sidebar.markdown(score_style, unsafe_allow_html=True)

# Display scores with better styling

# Display the score
st.sidebar.markdown("<div class='score-label'>得点：</div>", unsafe_allow_html=True)
st.sidebar.markdown(
    f"<div class='score-value'>{a_count} / {q_count}</div>", unsafe_allow_html=True
)


