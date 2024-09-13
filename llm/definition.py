import openai
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from parser.customJSONParser import JSONParser
from pydantic import ValidationError
from llm.promptTemplates import (
    answer_checking_prompt_gemini,
    answer_checking_prompt_openai,
    hint_generation_prompt_gemini,
    hint_generation_prompt_openai,
)

from parser.customStrParser import CustomStrOutputParser

# Initialize API keys
openai.api_key = st.secrets["openai"]
gemini_api_key = st.secrets["gemini"]


def create_judge_chain(model_class, model_name, api_key, prompt, variables) -> str:

    if model_class == ChatGoogleGenerativeAI:
        generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }
        model = model_class(
            model=model_name,
            api_key=api_key,
            model_kwargs=generation_config,
        )
    else:

        model = model_class(
            model=model_name,
            api_key=api_key,
            temperature=0,
            max_tokens=1611,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model_kwargs={"response_format": {"type": "json_object"}},
        )

    chain = prompt | model | JSONParser

    try:
        # Pass the variables to the chain
        response = chain.invoke(variables)

        # Return the filtered result
        return {
            "result": response["結果"],
            "reasoning": response["解説"],
        }

    except ValidationError as e:
        # Handle cases where the output is not valid or missing keys
        return {
            "error": "Invalid output. Required keys '結果' and '解説' are missing or incorrect format.",
            "details": str(e),
        }

    except Exception as e:
        # Catch other potential errors
        return {"error": "An unexpected error occurred.", "details": str(e)}


# Reusable function to create the chain
def create_hint_chain(model_class, model_name, api_key, prompt, variables) -> str:
    if model_class == ChatGoogleGenerativeAI:
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        model = model_class(
            model=model_name,
            api_key=api_key,
            model_kwargs=generation_config,
        )
    else:

        model = model_class(
            model=model_name,
            api_key=api_key,
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "text"},
        )

    chain = prompt | model | CustomStrOutputParser()
    # | StrOutputParser

    try:
        # Pass the variables to the chain
        response = chain.invoke(variables)

        # Return the filtered result
        return response

    except ValidationError as e:
        # Handle cases where the output is not valid or missing keys
        return {
            "error": "Invalid output. Required a string as the output",
            "details": str(e),
        }

    except Exception as e:
        # Catch other potential errors
        return {"error": "An unexpected error occurred.", "details": str(e)}


# Functions for Gemini LLM
def judge_gemini_chain(prompt, riddle) -> str:
    variables = {
        "question": riddle["question"],
        "correct_answer": riddle["correct_answer"],
        "user_answer": riddle["user_answer"],
    }

    try:
        return create_judge_chain(
            model_class=ChatGoogleGenerativeAI,
            model_name="gemini-1.5-pro",
            api_key=gemini_api_key,
            prompt=prompt,
            variables=variables,
        )
    except:
        return create_judge_chain(
            model_class=ChatGoogleGenerativeAI,
            model_name="gemini-1.5-flash",
            api_key=gemini_api_key,
            prompt=prompt,
            variables=variables,
        )


def hint_gemini_chain(prompt, riddle, hint, turn, reasoning) -> str:
    variables = {
        "question": riddle["question"],
        "correct_answer": riddle["correct_answer"],
        "hint_history": hint,
        "user_answer": riddle["user_answer"],
        "turn": turn,
        "reasoning": reasoning,
    }
    try:
        return create_hint_chain(
            model_class=ChatGoogleGenerativeAI,
            model_name="gemini-1.5-pro",
            api_key=gemini_api_key,
            prompt=prompt,
            variables=variables,
        )
    except:
        return create_judge_chain(
            model_class=ChatGoogleGenerativeAI,
            model_name="gemini-1.5-flash",
            api_key=gemini_api_key,
            prompt=prompt,
            variables=variables,
        )


# Functions for OpenAI LLM
def judge_openai_chain(prompt, riddle) -> str:
    variables = {
        "question": riddle["question"],
        "correct_answer": riddle["correct_answer"],
        "user_answer": riddle["user_answer"],
    }

    return create_judge_chain(
        model_class=ChatOpenAI,
        model_name="gpt-4o-mini",
        api_key=openai.api_key,
        prompt=prompt,
        variables=variables,
    )


def hint_openai_chain(prompt, riddle, hint, turn, reasoning) -> str:

    variables = {
        "question": riddle["question"],
        "correct_answer": riddle["correct_answer"],
        "hint_history": hint,
        "user_answer": riddle["user_answer"],
        "turn": turn,
        "reasoning": reasoning,
    }

    return create_hint_chain(
        model_class=ChatOpenAI,
        model_name="gpt-4o-mini",
        api_key=openai.api_key,
        prompt=prompt,
        variables=variables,
    )


# Code for modular test
if __name__ == "__main__":
    riddle = {
        "question": "からしはからしでも冷たいからしは？",
        "correct_answer": "木枯らし",
        "user_answer": "わさび",
    }
    turn = 0
    hint_history = []

    # gpt = judge_openai_chain(answer_checking_prompt_openai, riddle)
    # print(gpt)
    # reasoning = gpt["reasoning"]
    # hint_o = hint_openai_chain(
    #     hint_generation_prompt_openai, riddle, hint_history, turn, reasoning
    # )
    # print(hint_o)

    gemini = judge_gemini_chain(answer_checking_prompt_gemini, riddle)
    print(gemini)
    reasoning = gemini["reasoning"]
    hint_g = hint_gemini_chain(
        hint_generation_prompt_gemini, riddle, hint_history, turn, reasoning
    )
    print(hint_g)
