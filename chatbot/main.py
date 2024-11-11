"""
@author: Youwei Zheng
@target: Add partial sidebar
@update: 2024.11.11
"""

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from taipy.gui import Gui
from pages.home import page_home
from pages.chat import page_chat

# ------------------------------
# Main app
# ------------------------------

from pages.home import toggle_partial_sidebar


def on_init(state):
    toggle_partial_sidebar(state)


if __name__ == "__main__":
    print("Starting chatting with complete app...")

    gui = Gui(page=page_home, css_file="./main.css")
    partial_chat = gui.add_partial(page_chat)
    partial_sidebar = gui.add_partial("")

    gui.run(
        dark_mode=True,
        title="Chat Demo v4.0",
        watermark="Shanghai Exchange Group",
        use_reloader=True,
    )