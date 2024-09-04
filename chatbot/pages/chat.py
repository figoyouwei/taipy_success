"""
@author: Youwei Zheng
@target: chat page partial
@update: 2024.09.04
"""

import taipy.gui.builder as tgb
from taipy.gui import notify, Icon

from typing import List

# ------------------------------
# Initialize state variables
# ------------------------------

# NOTE: The user interacts with the Python interpreter only via css to change icon size
users: List[List[str]] = [
    ["Human", Icon("/icons/icon_hm.png")],
    ["AI", Icon("/icons/icon_ai.png")],
]

# * Initialize messages and empty_messages
empty_messages: List[List[str]] = [
    ["1", "Who are you?", "Human"],
    ["2", "Hi! I am GPT-4. How can I help you today?", "AI"],    
]
messages: List[List[str]] = empty_messages.copy()

# * Initialize past_messages
past_messages: List[List[List[str]]] = []

from tools.chat import chat_tongyi

def evaluate(state, var_name: str, payload: dict):
    """_summary_

    Args:
        state (_type_): _description_
        var_name (str): not sure of its function
        payload (dict): _description_
    """
    notify(state, "I", f"We are preparing your answer...")

    # Retrieve the callback parameters
    (_, _, message_hm, sender_id) = payload.get("args", [])
 
    # Add the input content as a sent message
    messages.append((f"{len(messages)}", message_hm, sender_id))
    # print(messages)
 
    # Default message used if evaluation fails
    result = "Invalid expression"
    try:
        # Evaluate the expression and store the result
        result = chat_tongyi(message_hm)
    except Exception:
        pass
 
    # Add the result as an incoming message
    messages.append((f"{len(messages)}", result, "AI"))

    state.messages = messages
    print(state.messages)

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as page_chat:
    # Doc for chat control: https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/chat/
    tgb.chat(
        "{messages}",
        users=users, 
        on_action=evaluate, 
        sender_id="Human"
    )
    
# ------------------------------
# Functions
# ------------------------------

from models.stateclass import ChatState

def reset_chat(state: ChatState) -> None:
    """
    Reset chat messages by clearing the conversation.

    Args:
        - state: The current state of the app.
    """

    print("The count of messages", len(state.messages))

    if len(state.messages) < 1:
        notify(state, "I", "No messages to reset")
        return

    state.past_messages += [(len(state.past_messages), state.messages)]

    print("empty_messages:", empty_messages)
    state.messages = empty_messages.copy()

    # state.context = initial_context
    state.partial_chat.update_content(state, page_chat)

    print("Chat was reset...")
    