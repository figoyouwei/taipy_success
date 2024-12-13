"""
@author: Youwei Zheng
@target: Add toggle partial sidebar
@update: 2024.12.12
"""

import uuid
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from taipy.gui import Gui
from pages.home import page_home
from pages.chat import page_chat

from pages.home import toggle_partial_sidebar

# ------------------------------
# on_init is created by taipy
# ------------------------------

user_session_id = None

def on_init(state):
    print("on_init: main_session.py")

    state.user_session_id = str(uuid.uuid4())[-6:]
    print("state.user_session_id: ", state.user_session_id)

    toggle_partial_sidebar(state)
    print("Finished toggle_partial_sidebar")
        
    # Add this line to ensure the partial has access to the state
    # state.partial_chat.update_state(state, page_chat)

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Starting running the app...")

    gui = Gui(page=page_home, css_file="./main.css")
    # Create partial without state_vars parameter
    partial_chat = gui.add_partial(page_chat)
    partial_sidebar = gui.add_partial("")

    print("Finished running the app...")
    
    gui.run(
        dark_mode=True,
        title="Chat Demo v4.0.1",
        watermark="Shanghai Exchange Group",
        use_reloader=True
    )
    
