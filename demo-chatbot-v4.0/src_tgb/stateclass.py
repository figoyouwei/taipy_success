from taipy.gui import State
from typing import List, Optional

import openai

class State(State):
    client: openai.Client
    initial_context: str
    context: str
    conversation: List[List[str]]
    users: List[List[str]]
    selected_conv: Optional[List[List[str]]]
    past_conversations: List[List[List[str]]]

