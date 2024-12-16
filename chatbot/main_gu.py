"""
@author: Youwei Zheng
@target: Make auth work with anonymous user
@update: 2024.12.16
"""

import os
import uuid
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

import taipy.gui.builder as tgb
from taipy.gui import Gui, State, navigate, notify
from taipy.core.config import Config
from taipy.auth import hash_taipy_password
import taipy.enterprise.gui as tp_enterprise

from pages.home import page_home, toggle_partial_sidebar
from pages.chat import page_chat

# ------------------------------
# auth related
# ------------------------------

os.environ["TAIPY_AUTH_HASH"] = "taipy"

username = None
password = None
credentials = None
login_dialog = True

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

# NOTE: on_init is created by taipy
def on_init(state):
    print("on_init: main_auth.py")
    state.user_session_id = str(uuid.uuid4())[-6:]
    print("state.user_session_id: ", state.user_session_id)

    state.sidebar_switch = False
    print("state.sidebar_switch: ", state.sidebar_switch)

# User login function
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

# Guest login function
def on_guest_login(state):
    # First close the login dialog
    state.login_dialog = False
    
    notify(state, "success", "Logged in as Guest...")

    try:
        # Navigate and render
        navigate(state, "home", force=False)
        toggle_partial_sidebar(state)
    except Exception as e:
        notify(state, "error", f"Login failed: {e}")
        print(f"Login exception: {e}")

# Root page
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