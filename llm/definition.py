import openai
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from parser.customJSONParser import JSONParser, JSONParserHint, CheckOutput
from langchain.prompts import PromptTemplate
from pydantic import ValidationError
from promptTemplates import answer_checking_prompt_gemini, answer_checking_prompt_openai

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
    else:
        generation_config = {
            "temperature": 0,
            "max_tokens": 1611,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "response_format": {"type": "json_object"},
        }

    model = model_class(
        model=model_name,
        api_key=api_key,
        generation_config=generation_config,
    )

    chain = prompt | model | JSONParser

    try:
        # Pass the variables to the chain
        response = chain.invoke(variables)
        parsed_response = CheckOutput.parse_raw(response)

        # Return the filtered result
        return {
            "result": parsed_response.結果,
            "reasoning": parsed_response.解説,
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
def create_hint_chain(
    model_class, model_name, api_key, temperature, prompt, variables
) -> str:
    model = model_class(model=model_name, api_key=api_key, temperature=temperature)

    chain = prompt | model | JSONParserHint
    # Pass the variables to the chain
    response = chain.invoke(variables)

    return response


# Functions for Gemini LLM
def judge_gemini_chain(prompt, riddle) -> str:
    variables = {
        "question": riddle["question"],
        "correct_answer": riddle["correct_answer"],
        "user_answer": riddle["user_answer"],
    }

    return create_judge_chain(
        model_class=ChatGoogleGenerativeAI,
        model_name="gemini-1.5-flash",
        api_key=gemini_api_key,
        prompt=prompt,
        variables=variables,
    )


def hint_gemini_chain(prompt, riddle, hint) -> str:
    variables = {
        "question": riddle["question"],
        "correct_answer": riddle["correct_answer"],
        "hint_hisotry": hint,
        "user_answer": riddle["user_answer"],
        "output_instruction": JSONParserHint.get_format_instructions(),
    }

    return create_hint_chain(
        model_class=ChatGoogleGenerativeAI,
        model_name="gemini-1.5-flash",
        api_key=gemini_api_key,
        temperature=0,
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
        temperature=0,
        prompt=prompt,
        variables=variables,
    )


def hint_openai_chain(prompt, riddle, hint) -> str:

    variables = {
        "question": riddle["question"],
        "correct_answer": riddle["correct_answer"],
        "hint_hisotry": hint,
        "user_answer": riddle["user_answer"],
        "output_instruction": JSONParserHint.get_format_instructions(),
    }

    return create_hint_chain(
        model_class=ChatOpenAI,
        model_name="gpt-4o-mini",
        api_key=openai.api_key,
        temperature=0.5,
        prompt=prompt,
        variables=variables,
    )


if __name__ == "__main__":
    riddle = {"question": "からしはからしでも冷たいからしは？", "answer": "木枯らし"}
    gpt = judge_openai_chain(answer_checking_prompt_openai, riddle)
    gemini = judge_gemini_chain(answer_checking_prompt_gemini, riddle)

    print(gpt)
    print(gemini)
