from taipy.gui import Gui, State
import taipy.gui.builder as tgb

show_dialog = False
some_content = "Hello, this is a pop-up"


# Initialize the state with 'show_dialog' to False
def on_init(state: State):
    state.show_dialog = False
    state.some_content = "Hello, this is a pop-up dialog!"


# Function to open the dialog
def open_dialog(state: State):
    state.show_dialog = True


# Function to close the dialog
def close_dialog(state: State):
    state.show_dialog = False


# ------------------------------
# table page
# ------------------------------

import pandas as pd

df_fruits = pd.DataFrame(
    {
        "fruits": ["apple", "banana", "apple", "banana", "banana"],
        "prices": [1.0, 2.0, 3.0, 4.0, 5.0],
    }
)

# print(df_fruits)
# print(type(df_fruits))

import taipy.gui.builder as tgb

with tgb.Page() as pagetable:
    tgb.text("Fruit Table")
    tgb.table("{df_fruits}")

# Build the page layout
with tgb.Page() as page:
    # Button to open the dialog
    tgb.button("Open Pop-up Table", on_action=open_dialog)

    # Dialog that will pop up when 'show_dialog' is True
    tgb.dialog(open="{show_dialog}", on_action=close_dialog, page="pagetable")

pages = {
    "/": "", 
    "page": page, 
    "pagetable": pagetable
    }

# Running the GUI
if __name__ == "__main__":
    gui = Gui(
        pages=pages,
        css_file="./dialog.css"
        )
    gui.run(dark_mode=True, title="Taipy Popup Table v4.0.0dev2")