from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

# Define the CheckOutput model
class CheckOutput(BaseModel):
    result: str = Field(
        description="It should be one of ['Correct', 'Incorrect']"
    )
    reasoning: str = Field(
        description="Explain the reason for the result shortly"
    )

# Initialize JSONParser using CheckOutput
JSONParser = JsonOutputParser(pydantic_object=CheckOutput)

class CheckOutputForHint(BaseModel):
    hint: str = Field(
        description="It should be a description"
    )
    reason: str = Field(
        description="Explain the reason for the hint shortly"
    )

# Initialize JSONParser using CheckOutput
JSONParserHint = JsonOutputParser(pydantic_object=CheckOutputForHint)