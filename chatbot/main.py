"""
@author: Youwei Zheng
@target: Main app
@update: 2024.09.04
"""

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from taipy.gui import Gui
from pages import page_sidebar, page_chat

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Starting chatting with complete app...")

    gui = Gui(page_sidebar)
    partial_chat = gui.add_partial(page_chat)

    gui.run(
        dark_mode=True, 
        title="Taipy Chat Demo v4.0"
        )