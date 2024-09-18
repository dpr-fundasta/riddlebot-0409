from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError
from langchain_core.output_parsers import JsonOutputParser
import json
import streamlit as st
import re


# Define the CheckOutput model
class CheckOutput(BaseModel):
    結果: str = Field(description="The result of the Riddle game")
    解説: str = Field(description="Reasoning of the result")


# class CustomJsonParser(JsonOutputParser):
#     def parse(self, output: str) -> dict:
#         cleaned_output = self.clean_output(output)

#         try:
#             parsed = json.loads(cleaned_output)
#             result = {"結果": parsed.get("結果", ""), "解説": parsed.get("解説", "")}
#             validated_output = CheckOutput(**result)
#             return validated_output.dict()

#         except json.JSONDecodeError as e:
#             st.session_state.error = e
#             raise ValueError(f"Failed to parse JSON: {e}")

#         except ValidationError as e:
#             st.session_state.error = e
#             raise ValueError(f"JSON Validation failed: {e}")

#     def clean_output(self, output: str) -> str:
#         # Remove markdown code block syntax
#         output = re.sub(r"```json|```", "", output).strip()

#         # Extract JSON content
#         json_match = re.search(r"\{.*\}", output, re.DOTALL)
#         if json_match:
#             output = json_match.group(0)
#         else:
#             # If no JSON content is found, return an empty JSON object
#             return "{}"

#         # Remove unwanted backslashes and escape sequences
#         output = output.replace("\\\n", "")  # Remove backslash followed by newline
#         output = output.replace("\\n", " ")  # Replace escaped newline with space
#         output = output.replace("\\", "")  # Remove any remaining backslashes

#         # Remove any remaining newlines and extra whitespace
#         output = re.sub(r"\s+", " ", output).strip()

#         return output


# Initialize JSONParser using CheckOutput
JSONParser = JsonOutputParser(pydantic_object=CheckOutput)
