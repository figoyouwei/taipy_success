"""
@author: Youwei Zheng
@target: chat page partial
@update: 2024.12.18
"""

import taipy.gui.builder as tgb
from taipy.gui import notify, Icon

from typing import List, Optional, Any

from models.chat import ChatMessage, ChatSession, SessionCollection

# ------------------------------
# Initialize empty messages
# ------------------------------

def create_initial_chat_session(user_session_id: str):
    return ChatSession(
        user_session_id=user_session_id,
        messages=[
            ChatMessage(message_id=1, content="Who are you?", sender="Human"),
            ChatMessage(message_id=2, content="Hi! I am GPT-4. How can I help you today?", sender="Robot"),
        ]
    )

# ------------------------------
# Initialize state variables
# ------------------------------

# NOTE: The user interacts with the Python interpreter only via css to change icon size
users: List[List[str]] = [
    ["Human", Icon("icons/icon_guest.png")],
    ["Robot", Icon("icons/icon_ai.png")],
]

# * Initialize chat session as current session
empty_messages = []  # Remove the initial assignment here
print("empty_messages: ", empty_messages)

# * Initialize selected conversation and history conversations which contain messages
chat_session = ChatSession(messages=empty_messages, user_session_id="")
messages = chat_session.to_list()

selected_session = ChatSession(messages=[], user_session_id="") 
session_collection = SessionCollection(user_session_id="")
sessions = session_collection.sessions

# ------------------------------
# Functions
# ------------------------------

from tools.chatrag import chat_suaee
from tools.chatcpl import chat_openai
from tools.chatcpl import chat_tongyi_naive

chatllm = chat_openai

# Example usage in evaluate function
# Note: var_name is not very important in the chat context.
def evaluate(state, var_name: str, payload: dict):
    chatbot = state.chatllm

    notify(state, "I", f"We are preparing your answer...")
    print("We are preparing your answer for user: ", state.user_session_id)

    print("chat_session.user_session_id: ", state.chat_session.user_session_id)

    # Initialize chat_session if it doesn't exist or user_session_id is empty
    if state.chat_session is None or state.chat_session.user_session_id == "":
        state.chat_session = create_initial_chat_session(state.user_session_id)
        print("chat_session initialized with user_session_id: ", state.user_session_id)

    # Retrieve the callback parameters
    (_, _, message_hm, sender_id) = payload.get("args", [])
    
    # Default message used if evaluation fails
    result = "Invalid expression"
    try:
        # Evaluate the expression and store the result
        result = chatbot(message_hm)
    except Exception:
        pass

    # Append human message
    state.chat_session.add_message(content=message_hm, sender="Human")
    state.chat_session.add_message(content=result, sender="Robot")

    print("session updated...")
    print(state.chat_session)

    # NOTE: update messages
    state.messages = state.chat_session.to_list()

    # NOTE: update frontend
    state.partial_chat.update_content(state, page_chat)

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as page_chat:   
    # Doc for chat control: https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/chat/
    tgb.chat(
        # Note: messages is actually the "var_name" in the evaluate function
        messages="{messages}", 
        users=users,
        on_action=evaluate, 
        sender_id="Human",
        # NOTE: to solve icon issue
        show_sender=True,
        height="80vh",
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

    # Validate user_session_id
    if not hasattr(state, 'user_session_id') or not state.user_session_id:
        notify(state, "E", "User session ID is required")
        return

    # Initialize session_collection with error handling
    try:
        if state.session_collection is None or state.session_collection.user_session_id != state.user_session_id:
            state.session_collection = SessionCollection(user_session_id=state.user_session_id)
    except Exception as e:
        notify(state, "E", f"Failed to initialize session: {str(e)}")
        return

    print("session_collection initialized...")
    print(state.chat_session)

    # Check if there are any messages to save
    if len(state.chat_session.messages) <= 2:
        notify(state, "I", "No messages to reset")
        return

    # Check if the current session already exists in the session_collection
    existing_session = next((s for s in state.session_collection.sessions 
                           if s.chat_session_id == state.chat_session.chat_session_id 
                           and s.user_session_id == state.user_session_id), None)

    if existing_session:
        existing_session.update_messages(state.chat_session.messages)
    else:
        # Ensure chat session has correct user_session_id before adding
        state.chat_session.user_session_id = state.user_session_id
        state.session_collection.add_session(state.chat_session)

    # Calculate the new session number for this user
    user_sessions = [s for s in state.session_collection.sessions 
                    if s.user_session_id == state.user_session_id]
    new_session_no = len(user_sessions) + 1

    # Create new session with validated user_session_id
    state.chat_session = ChatSession(
        user_session_id=state.user_session_id,
        chat_session_no=new_session_no,
        messages=empty_messages
    )
    print(f"A new session with chat_session_no {new_session_no} and user_session_id {state.user_session_id} has been created.")
    print(state.chat_session)

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
    for message in messages:
        if message.message_id == message_id:
            return message.content[:20]
    return "Message not found"

def selector_adapter(sess: ChatSession):
    message_title = get_message_title_by_id(sess.messages, 3)
    return (sess.chat_session_no, message_title)

# ------------------------------
# State Initialization
# ------------------------------

def init_chat(state):
    """Initialize all chat-related state variables"""
    if not hasattr(state, 'user_session_id') or not state.user_session_id:
        print("Warning: init_chat called without valid user_session_id")
        return
        
    print(f"Initializing chat for user: {state.user_session_id}")
    
    # Create a fresh session collection
    state.session_collection = SessionCollection(user_session_id=state.user_session_id)
    state.sessions = []
    
    # Create a completely new chat session
    state.chat_session = create_initial_chat_session(state.user_session_id)
    state.messages = state.chat_session.to_list()
    
    # Reset selected session
    state.selected_session = ChatSession(messages=[], user_session_id=state.user_session_id)
    
    print(f"Chat initialized with session: {state.chat_session}")