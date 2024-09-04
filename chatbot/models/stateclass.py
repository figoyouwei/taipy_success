from taipy.gui import State
from typing import List, Optional

import openai

class ChatState(State):
    """Dedicated class to manage chat sessions.

    Args:
        State (_type_): _description_
    """

    client: None
    initial_context: str
    users: List[List[str]]
    context: str
    messages: List[List[str]]
    selected_messages: Optional[List[List[str]]]
    past_messages: List[List[List[str]]]

