"""
@author: Youwei Zheng
@target: Make auth work with anonymous user
@update: 2024.12.16
"""

import uuid
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

import taipy.gui.builder as tgb
from taipy.gui import Gui, State, navigate, notify
from taipy.core.config import Config

from pages.home import page_home, toggle_partial_sidebar
from pages.chat import page_chat

# ------------------------------
# enterprise imports
# ------------------------------

import taipy.enterprise.gui as tp_enterprise
from taipy.auth import hash_taipy_password

# ------------------------------
# auth related
# ------------------------------

os.environ["TAIPY_AUTH_HASH"] = "taipy"

username = None
password = None
credentials = None
login_dialog = True # default login dialog important for login page rendering

passwords = {
    "figo": hash_taipy_password("figo76"),
    "alex": hash_taipy_password("alex24"),
}

roles = {
    "figo": ["admin", "staff"],
    "alex": ["reader"],
}

Config.configure_authentication(
    "taipy", 
    passwords=passwords, 
    roles=roles,
    auth_required=True
)

user_session_id = None
sidebar_switch = False

# ------------------------------
# on_init
# ------------------------------

def on_init(state):
    print("on_init: main_gu.py")

    state.user_session_id = str(uuid.uuid4())[-6:]
    print("state.user_session_id: ", state.user_session_id)

    state.sidebar_switch = False
    print("state.sidebar_switch: ", state.sidebar_switch)

# ------------------------------
# User login function
# ------------------------------

def on_user_login(state):
    try:
        # Use the state.username and state.password that are bound to the input fields
        state.credentials = tp_enterprise.login(state, state.username, state.password)
        state.login_dialog = False  # Close the login dialog
        notify(state, "success", f"Logged in as User {state.username}...")
        navigate(state, "home", force=False)
        toggle_partial_sidebar(state)
    except Exception as e:
        notify(state, "error", f"Login failed: {e}")
        print(f"Login exception: {e}")
        navigate(state, to="login", force=False)

# ------------------------------
# Guest login function
# ------------------------------

def on_guest_login(state):
    # First close the login dialog
    state.login_dialog = False
    print("state.login_dialog: ", state.login_dialog)

    state.user_session_id = str(uuid.uuid4())[-6:]
    print("state.user_session_id: ", state.user_session_id)

    state.sidebar_switch = False
    print("state.sidebar_switch: ", state.sidebar_switch)
    
    notify(state, "success", "Logged in as Guest...")

    try:
        # Navigate and render
        navigate(state, "home", force=False)
        toggle_partial_sidebar(state)
    except Exception as e:
        notify(state, "error", f"Login failed: {e}")
        print(f"Login exception: {e}")

# ------------------------------
# Logout function
# ------------------------------

def on_logout(state):
    try:
        # Reset auth-related state variables
        state.username = None
        state.password = None
        state.credentials = None
        state.login_dialog = True
        state.user_session_id = str(uuid.uuid4())[-6:]  # Generate new session ID
        state.sidebar_switch = False
        
        # Reset all chat-specific variables
        empty_messages = create_initial_chat_session("").messages
        state.chat_session = ChatSession(messages=empty_messages, user_session_id="")
        state.messages = state.chat_session.to_list()
        
        state.selected_session = ChatSession(messages=[], user_session_id="")
        state.session_collection = SessionCollection()
        state.sessions = state.session_collection.sessions
        
        # Logout from taipy enterprise
        tp_enterprise.logout(state)
        
        # Notify user
        notify(state, "success", "Logged out successfully")
        
        # Navigate back to login page
        navigate(state, "login", force=True)
        
    except Exception as e:
        notify(state, "error", f"Logout failed: {e}")
        print(f"Logout exception: {e}")

# ------------------------------
# Root page
# ------------------------------

with tgb.Page() as login_page:
    with tgb.dialog("{login_dialog}", title="Welcome!"):
        tgb.input("{username}", label="Username")
        tgb.input("{password}", label="Password", password=True)
        tgb.html("hr")
        with tgb.layout("1 1 1"):
            with tgb.part():
                tgb.text("")
            with tgb.part():
                tgb.button("Guest Login", class_name="fullwidth", on_action=on_guest_login)
            with tgb.part():
                tgb.button("User Login", class_name="fullwidth plain", on_action=on_user_login)

# Define page routing
root_page = tgb.Page(on_init=on_init)

pages = {
    "/": root_page,
    "login": login_page,
    "home": page_home,
}

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Starting chatting with complete app...")

    gui = Gui(pages=pages, css_file="./main.css")
    partial_chat = gui.add_partial(page_chat)
    partial_sidebar = gui.add_partial("")

    gui.run(
        dark_mode=True,
        title="Chat Demo with Auth",
        watermark="Shanghai Exchange Group",
        use_reloader=True
    )