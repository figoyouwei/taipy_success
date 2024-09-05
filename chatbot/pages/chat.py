"""
@author: Youwei Zheng
@target: chat page partial
@update: 2024.09.05
"""

import taipy.gui.builder as tgb
from taipy.gui import notify, Icon

from typing import List, Optional

# ------------------------------
# Initialize state variables
# ------------------------------

# NOTE: The user interacts with the Python interpreter only via css to change icon size
users: List[List[str]] = [
    ["Human", Icon("/icons/icon_hm.png")],
    ["AI", Icon("/icons/icon_ai.png")],
]

# * Initialize empty_messages
empty_messages: List[List[str]] = [
    ["1", "Who are you?", "Human"],
    ["2", "Hi! I am GPT-4. How can I help you today?", "AI"],    
]

# * Initialize current messages
messages: List[List[str]] = empty_messages.copy()

# * Initialize selected conversation and history conversations which contain messages
selected_session: Optional[List[List[str]]] = None
chat_sessions: List[List[List[str]]] = []

# ------------------------------
# Functions
# ------------------------------

from tools.chat import chat_tongyi_without_memory

def evaluate(state, var_name: str, payload: dict):
    """_summary_

    Args:
        state (_type_): _description_
        var_name (str): not sure of its function
        payload (dict): _description_
    """
    notify(state, "I", f"We are preparing your answer...")
    print("New round of paired messages...")

    # Retrieve the callback parameters
    (_, _, message_hm, sender_id) = payload.get("args", [])
 
    # Append human message
    state.messages.append((f"{len(state.messages)+1}", message_hm, sender_id))
    # print(messages)
 
    # Default message used if evaluation fails
    result = "Invalid expression"
    try:
        # Evaluate the expression and store the result
        result = chat_tongyi_without_memory(message_hm)
    except Exception:
        pass
 
    # Append AI message
    state.messages.append((f"{len(state.messages)+1}", result, "AI"))
    # print(state.messages)

    # NOTE: update chat.content
    state.partial_chat.update_content(state, page_chat)

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
# Function: reset chat messages
# ------------------------------

def reset_chat(state) -> None:
    """
    Reset chat messages by clearing the conversation.

    Args:
        - state: The current state of the app.
    """

    print("The user is resetting chat...")

    # ! Why selector adapter is coming here?

    # NOTE: save messages to history_conversations
    state.chat_sessions += [(len(state.chat_sessions), state.messages)]
    print("Current messages were saved into history_conversations with an index")
    print(state.chat_sessions)
    
    if len(state.messages) < 3:
        notify(state, "I", "No messages to reset")
        return

    # NOTE: reset messages by empty_messages
    state.messages = empty_messages.copy()

    # NOTE: reset chat.content
    state.partial_chat.update_content(state, page_chat)
    print("Chat was reset...")
    
# ------------------------------
# Function: select session
# ------------------------------

def select_session(state, var_name: str, value) -> None:
    """
    Display the messages of selected conversation from history_conversations in tgb.chat()

    Args:
        state: The current state of the app.
        var_name: "selected_conv"
        value: [[id, conversation]]
    """

    print("The user selected a session...")
    print(state.selected_session)

    # NOTE: selected session to messages
    state.messages = state.selected_session[1]
    state.partial_chat.update_content(state, page_chat)
    print("messages updated...")

# ------------------------------
# Function: selector adapter
# ------------------------------

def selector_adapter(item: list):
    """
    Converts element of history_conversations to (id and displayed string)?

    Args:
        item: element of history_conversations

    Returns:
        id and displayed string
    """
    print("Entering selector adapter")

    # TODO: It has to reference to that id in the history_conversations to not repeat sessions
    # NOTE: The function that transforms an element of lov into a tuple(id:str, label:str|Icon).
    print("item", item, type(item))

    conversation = item[1]
    last_message_info = conversation[len(conversation) - 1]
    last_message = last_message_info[1]
    return (str(item[0]), last_message[:50] + "...")
