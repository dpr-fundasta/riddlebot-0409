from langchain_core.output_parsers import StrOutputParser
from langchain.schema import AIMessage


class CustomStrOutputParser(StrOutputParser):
    def parse(self, output: any) -> str:
        # Check if the output is an AIMessage object
        if isinstance(output, AIMessage):
            return output.content  # Extract the content of AIMessage
        elif isinstance(output, str):
            return output  # Handle the plain text case
        else:
            raise ValueError(
                f"Expected plain text or AIMessage, but got {type(output)}"
            )

    def get_format_instructions(self) -> str:
        # Optionally, provide format instructions
        return "Return plain text or extract content from AIMessage."
