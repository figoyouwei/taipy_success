"""
@author: Youwei Zheng
@target: chat page partial
@update: 2024.09.06
"""

import taipy.gui.builder as tgb
from taipy.gui import notify, Icon

from typing import List, Optional, Any

from models.chat import ChatMessage, ChatSession, SessionCollection

# ------------------------------
# Initialize state variables
# ------------------------------

# NOTE: The user interacts with the Python interpreter only via css to change icon size
users: List[List[str]] = [
    ["Human", Icon("/icons/icon_hm.png")],
    ["AI", Icon("/icons/icon_ai.png")],
]

# * Initialize empty messages
empty_messages = [
    ChatMessage(id=1, content="Who are you?", sender="Human"),
    ChatMessage(id=2, content="Hi! I am GPT-4. How can I help you today?", sender="AI"),
]

# * Initialize chat session as current session
chat_session = ChatSession(messages=empty_messages)
messages = chat_session.to_list()

# * Initialize selected conversation and history conversations which contain messages
selected_session = ChatSession(messages=[])
session_collection = SessionCollection()
sessions = session_collection.sessions

# ------------------------------
# Functions
# ------------------------------

from tools.chat import chat_tongyi_without_memory

# Example usage in evaluate function
def evaluate(state, var_name: str, payload: dict):
    notify(state, "I", f"We are preparing your answer...")
    print("We are preparing your answer...")

    # Retrieve the callback parameters
    (_, _, message_hm, sender_id) = payload.get("args", [])

    # Append human message
    state.chat_session.add_message(content=message_hm, sender=sender_id)

    # Default message used if evaluation fails
    result = "Invalid expression"
    try:
        # Evaluate the expression and store the result
        result = chat_tongyi_without_memory(message_hm)
    except Exception:
        pass

    # Append AI message
    state.chat_session.add_message(content=result, sender="AI")
    state.messages = state.chat_session.to_list()

    # NOTE: update chat.content
    state.partial_chat.update_content(state, page_chat)

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as page_chat:
    # Doc for chat control: https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/chat/
    tgb.chat(
        messages="{messages}",
        users=users, 
        on_action=evaluate, 
        sender_id="Human"
    )
    
# ------------------------------
# Function: reset chat messages
# ------------------------------

def reset_session(state) -> None:
    """
    Reset chat messages by clearing the conversation and saving the current session to history.

    Args:
        - state: The current state of the app, including chat_sessions and the current session.
    """

    print("The user is resetting chat...")

    # Initialize session_collection if it doesn't exist
    if state.session_collection is None:
        state.session_collection = SessionCollection()

    # Check if there are any messages to save
    if len(state.chat_session.messages) <= 2:
        notify(state, "I", "No messages to reset")
        return

    # Check if the current session already exists in the session_collection
    existing_session = next((s for s in state.session_collection.sessions if s.session_id == state.chat_session.session_id), None)

    if existing_session:
        # Update the existing session's messages using the new method
        existing_session.update_messages(state.chat_session.messages)
    else:
        # Add the current session to the collection
        state.session_collection.add_session(state.chat_session)
        print(f"Current session with id {state.chat_session.session_id} was added to the session collection.")

    print(state.session_collection.sessions)

    # Calculate the new session number
    new_session_no = len(state.session_collection.sessions) + 1

    # Create a new ChatSession with the incremented session_no (starting from 1)
    state.chat_session = ChatSession(session_no=new_session_no, messages=empty_messages)
    print(f"A new session with session_no {new_session_no} has been created.")

    # NOTE: update chat
    state.messages = state.chat_session.to_list()
    state.partial_chat.update_content(state, page_chat)
    print("Chat was reset...")

    # NOTE: update selector list
    state.sessions = state.session_collection.sessions
    print("Selector list was updated...")
        
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

    # # NOTE: selected session to messages
    state.chat_session = state.selected_session
    state.messages = state.chat_session.to_list()

    state.partial_chat.update_content(state, page_chat)
    print("chat session updated...")

# ------------------------------
# Function: selector adapter
# ------------------------------

def get_message_title_by_id(messages: List[ChatMessage], message_id: int) -> str:
    # Find the message with the given id
    for message in messages:
        if message.id == message_id:
            # Return the last 10 characters of the content
            return message.content[:20]
    return "Message not found"

def selector_adapter(sess: ChatSession):
    # NOTE: The function that transforms a data model into a tuple(id:str, label:str).
    message_title = get_message_title_by_id(sess.messages, 3)
    return (sess.session_no, message_title)