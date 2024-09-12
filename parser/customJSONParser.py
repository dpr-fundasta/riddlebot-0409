from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


# Define the CheckOutput model
class CheckOutput(BaseModel):
    結果: str = Field(description="The result of the Riddle game")
    解説: str = Field(description="Reasoning of the result")


# Initialize JSONParser using CheckOutput
JSONParser = JsonOutputParser(pydantic_object=CheckOutput)


class CheckOutputForHint(BaseModel):
    hint: str = Field(description="It should be a description")
    reason: str = Field(description="Explain the reason for the hint shortly")


# Initialize JSONParser using CheckOutput
JSONParserHint = JsonOutputParser(pydantic_object=CheckOutputForHint)
