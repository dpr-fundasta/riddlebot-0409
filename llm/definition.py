import openai
import streamlit as st
import re
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
from langchain_core.exceptions import OutputParserException
from google.api_core.exceptions import InternalServerError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import json


# Initialize API keys
openai.api_key = st.secrets["openai"]
gemini_api_key = st.secrets["gemini"]


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(3),
    retry=retry_if_exception_type(InternalServerError),
)
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

        if "結果" not in response or "解説" not in response:
            raise KeyError("Missing required keys '結果' and/or '解説' in response")

        # Return the filtered result
        return {
            "result": response["結果"],
            "reasoning": response["解説"],
        }

  

    except OutputParserException as e:
        # print(f"Error in create_judge_chain: {str(e)}")
        # invalid_output = str(e).split("Invalid json output:")[-1].strip()
        # # Clean the invalid JSON string
        # response = clean_json_string(invalid_output)
        # if "結果" not in response or "解説" not in response:
        #     raise KeyError("Missing required keys '結果' and/or '解説' in response")
        return {
            "result": "Incorrect",
            "reasoning": "LLMはこのなぞなぞの結果と推論を生成することができなかった。",
        }

    except (ValidationError, KeyError, json.JSONDecodeError) as e:
        print(f"Error in create_judge_chain: {str(e)}")
        return {
            "error": "Invalid output format or missing required keys.",
            "details": str(e),
        }

    except Exception as e:
        st.session_state.error = e
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
        "output_instruction": JSONParser.get_format_instructions(),
    }

    return create_judge_chain(
        model_class=ChatGoogleGenerativeAI,
        model_name="gemini-1.5-pro",
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
    return create_hint_chain(
        model_class=ChatGoogleGenerativeAI,
        model_name="gemini-1.5-pro",
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
        "output_instruction": JSONParser.get_format_instructions(),
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


def clean_json_string(output):
    output = output.strip("`").strip()
    # Remove 'json' prefix
    if output.startswith("json"):
        output = output[len("json") :].strip()
    # Remove backslash-newline sequences
    output = re.sub(r"\\\s*[\r\n]+", "", output)
    # Escape any remaining backslashes
    output = output.replace("\n", "")

    return json.loads(output)

