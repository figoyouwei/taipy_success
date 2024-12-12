"""
@author: Youwei Zheng
@target: Make auth work
@update: 2024.12.12
"""

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

import taipy.gui.builder as tgb
from taipy.gui import Gui, State, navigate, notify
from taipy.core.config import Config
from taipy.auth import hash_taipy_password
import taipy.enterprise.gui as tp_enterprise

from pages.home import page_home
from pages.chat import page_chat

import pandas as pd

# ------------------------------
# Main app
# ------------------------------

from pages.home import toggle_partial_sidebar

os.environ["TAIPY_AUTH_HASH"] = "taipy"

username = None
credentials = None

passwords = {
    "florian": hash_taipy_password("flower"),
    "alex": hash_taipy_password("alex24"),
}

roles = {
    "florian": ["admin", "staff"],
    "alex": ["reader"],
}

Config.configure_authentication(
    "taipy", 
    passwords=passwords, 
    roles=roles,
    auth_required=True
)

def on_init(state):
    navigate_to_login(state)

# Login function
def on_login(state: State, id, login_args):
    # Extract username and password from login_args
    state.username, password = login_args["args"][:2]
    print(f"Username: {state.username}, Password: {password}")
    try:
        # Attempt to log in using Taipy Enterprise
        state.credentials = tp_enterprise.login(state, state.username, password)
        notify(state, "success", f"Logged in as {state.username}...")
        navigate(state, "home", force=False)
        toggle_partial_sidebar(state)
    except Exception as e:
        notify(state, "error", f"Login failed: {e}")
        print(f"Login exception: {e}")
        navigate(state, to="login", force=False)

# Function to navigate to the login page
def navigate_to_login(state: State):
    navigate(state=state, to="login", force=False)
    
root_page = ""

# Define login page
with tgb.Page() as page_login:
    tgb.login("Welcome to Chat!")

# Define page routing
pages = {
    "/": root_page,
    "home": page_home,
    "login": page_login,
}

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