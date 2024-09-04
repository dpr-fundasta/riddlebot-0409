import openai
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from parser.customJSONParser import JSONParser, JSONParserHint
from langchain.prompts import PromptTemplate

# Initialize API keys
openai.api_key = st.secrets["openai"]
gemini_api_key = st.secrets["gemini"]


def create_judge_chain(model_class, model_name, api_key, temperature, prompt, variables) -> str:
    model = model_class(
        model=model_name,
        api_key=api_key,
        temperature=temperature
    )
    
    chain = prompt | model | JSONParser

    # Pass the variables to the chain
    response = chain.invoke(variables)
    
    return response

# Reusable function to create the chain
def create_hint_chain(model_class, model_name, api_key, temperature, prompt, variables) -> str:
    model = model_class(
        model=model_name,
        api_key=api_key,
        temperature=temperature
    )
    
    chain = prompt | model | JSONParserHint
    # Pass the variables to the chain
    response = chain.invoke(variables)
    
    return response

# Functions for Gemini LLM
def judge_gemini_chain(prompt, riddle) -> str:
    variables = {
        "question": riddle['question'],
        "correct_answer": riddle['correct_answer'],
        
        "user_answer": riddle['user_answer'],
        "output_instruction": JSONParser.get_format_instructions(),
    }
    
    return create_judge_chain(
        model_class=ChatGoogleGenerativeAI,
        model_name="gemini-1.5-flash",
        api_key=gemini_api_key,
        temperature=0,
        prompt=prompt,
        variables=variables
    )

def hint_gemini_chain(prompt, riddle, hint) -> str:
    variables = {
        "question": riddle['question'],
        "correct_answer": riddle['correct_answer'],
        "hint_hisotry":hint,
        "user_answer": riddle['user_answer'],
        "output_instruction": JSONParserHint.get_format_instructions(),
    }
        
    return create_hint_chain(
        model_class=ChatGoogleGenerativeAI,
        model_name="gemini-1.5-flash",
        api_key=gemini_api_key,
        temperature=0,
        prompt=prompt,
        variables=variables
    )

# Functions for OpenAI LLM
def judge_openai_chain(prompt, riddle) -> str:
    variables = {
        "question": riddle['question'],
        "correct_answer": riddle['correct_answer'],
        
        "user_answer": riddle['user_answer'],
        "output_instruction": JSONParser.get_format_instructions(),
    }
    
    return create_judge_chain(
        model_class=ChatOpenAI,
        model_name="gpt-4o-mini",
        api_key=openai.api_key,
        temperature=0,
        prompt=prompt,
        variables=variables
    )

def hint_openai_chain(prompt, riddle, hint) -> str:

    variables = {
        "question": riddle['question'],
        "correct_answer": riddle['correct_answer'],
        "hint_hisotry":hint,
        "user_answer": riddle['user_answer'],
        "output_instruction": JSONParserHint.get_format_instructions(),
    }
    
    return create_hint_chain(
        model_class=ChatOpenAI,
        model_name="gpt-4o-mini",
        api_key=openai.api_key,
        temperature=0.5,
        prompt=prompt,
        variables=variables 
    )
