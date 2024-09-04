from taipy.gui import State
from typing import List, Optional

# ? What's the point of this class?

class ChatState(State):
    """Dedicated class to manage chat sessions.

    Args:
        State (_type_): _description_
    """

    users: List[List[str]]
    messages: List[List[str]]
    past_messages: List[List[List[str]]]
