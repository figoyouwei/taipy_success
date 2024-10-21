"""
@author: Youwei Zheng
@target: Solved icon-display issue with Taipy v4.0.0
@update: 2024.10.15
"""

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from taipy.gui import Gui
from pages.home import page_home
from pages.chat import page_chat

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Starting chatting with complete app...")

    gui = Gui(
        page=page_home,
        css_file="./main.css"
        )
    partial_chat = gui.add_partial(page_chat)

    gui.run(
        dark_mode=True,
        title="Taipy Chat Demo v4.0.0"
        )