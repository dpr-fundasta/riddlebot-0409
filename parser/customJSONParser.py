from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser


# Define the CheckOutput model
class CheckOutput(BaseModel):
    結果: str = Field(
        description="判定結果必ず'Correct'か'Incorrect'で答えてください。"
    )
    解説: str = Field(description="判定結果の理由")


JSONParser = JsonOutputParser(pydantic_object=CheckOutput)
