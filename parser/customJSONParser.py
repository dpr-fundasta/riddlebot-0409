from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError
from langchain_core.output_parsers import JsonOutputParser
import json
import streamlit as st
import re


# Define the CheckOutput model
class CheckOutput(BaseModel):
    結果: str = Field(description="The result of the Riddle game")
    解説: str = Field(description="Reasoning of the result")


class CustomJsonParser(JsonOutputParser):
    def parse(self, output: str) -> dict:
        cleaned_output = self.clean_output(output)

        try:
            parsed = json.loads(cleaned_output)
        except json.JsonDecodeError as e:
            st.session_state.error = e
            raise ValueError(f"Failed to parse JSON: {e}")

        try:
            validated_output = self.pydantic_object(**parsed)
        except ValidationError as e:
            st.session_state.error = e
            raise ValueError(f"JSON Validation failed: {e}")
        return validated_output.dict()


def clean_output(self, output: str) -> str:
    try:
        fixed = output.replace("\\\n", "").replace("\n", "")
        cleaned = re.sub(r"[\\\n\r\t]", "", fixed)
        return cleaned
    except Exception as e:
        st.session_state.error = e
        raise ValueError(f"Error while cleaning output: {e}")


# Initialize JSONParser using CheckOutput
JSONParser = CustomJsonParser(pydantic_object=CheckOutput)


# class CheckOutputForHint(BaseModel):
#     hint: str = Field(description="It should be a description")
#     reason: str = Field(description="Explain the reason for the hint shortly")


# # Initialize JSONParser using CheckOutput
# JSONParserHint = JsonOutputParser(pydantic_object=CheckOutputForHint)
