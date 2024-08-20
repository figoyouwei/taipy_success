from typing import List, Dict, Any
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Summary(BaseModel):
    summary: str = Field(description="Summary")
    facts: List[str] = Field(description="Facts")

parser_summary = PydanticOutputParser(pydantic_object=Summary)

# s = Summary(
#     summary="It is a summary.",
#     facts=[
#         "Interesting",
#         "Very interesting"
#     ]
# )

# s.__dict__