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
import logging

# Configure logging
logging.basicConfig(
    filename='riddlebot.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Initialize API keys
openai.api_key = st.secrets["openai"]
gemini_api_key = st.secrets["gemini"]


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(0.5),
    retry=retry_if_exception_type(InternalServerError, KeyError, json.JSONDecodeError, ValueError),
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
        logging.error(f"OutputParserException in create_judge_chain: {str(e)}")
        invalid_output = str(e).split("Invalid json output:")[-1].strip()
        # Clean the invalid JSON string
        try:
            response = clean_json_string(invalid_output)
            if "error" in response:
                return response  # Return the error message if the JSON was invalid

            if "結果" not in response or "解説" not in response:
                raise KeyError("Missing required keys '結果' and/or '解説' in response")

            return {
                "result": response["結果"],
                "reasoning": response["解説"],
            }
        except json.JSONDecodeError as json_err:
            logging.error(f"JSONDecodeError in create_judge_chain after clean_json_string: {str(json_err)}")
            return {
                "error": "The system encountered an issue processing the response. Please try again later.",
                "details": str(json_err),
            }

    except (ValidationError, KeyError, ValueError, json.JSONDecodeError) as e:
        logging.error(f"ValidationError/KeyError/JSONDecodeError in create_judge_chain: {str(e)}")
        return {
            "error": "Invalid output format or missing required keys.",
            "details": str(e),
        }

    except Exception as e:
        logging.error(f"Unexpected error in create_judge_chain: {str(e)}")
        # Optionally, you can store the error in session state or handle it as needed
        st.session_state.error = str(e)
        # Return a general error message without exposing details
        return {"error": "An unexpected error occurred. Please try again later."}


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
        logging.error(f"ValidationError in create_hint_chain: {str(e)}")
        # Handle cases where the output is not valid or missing keys
        return {
            "error": "Invalid output. Required a string as the output.",
            "details": str(e),
        }

    except Exception as e:
        logging.error(f"Unexpected error in create_hint_chain: {str(e)}")
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
    """
    Cleans and parses a JSON string.

    Args:
        output (str): The raw output string to be cleaned and parsed.

    Returns:
        dict: The parsed JSON as a dictionary.

    Raises:
        json.JSONDecodeError: If the output cannot be decoded as JSON.
    """
    output = output.strip("`").strip()
    # Remove 'json' prefix
    if output.startswith("json"):
        output = output[len("json"):].strip()
    # Remove backslash-newline sequences
    output = re.sub(r"\\\s*[\r\n]+", "", output)
    # Escape any remaining backslashes
    output = output.replace("\n", "")

    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        logging.error(f"JSONDecodeError in clean_json_string: {str(e)} | Output: {output}")
        raise  # Re-raise the exception to be handled by the caller
