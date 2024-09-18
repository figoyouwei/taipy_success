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


# Import table page
from page_table import page as pagetable

# Build the page layout
with tgb.Page() as page:
    # Button to open the dialog
    tgb.button("Open Pop-up Table", on_action=open_dialog)

    # Dialog that will pop up when 'show_dialog' is True
    with tgb.dialog(open="{show_dialog}", on_action=close_dialog, partial=pagetable):
        with tgb.layout(columns="1"):
            tgb.part(class_name="p2", partial="{pagetable}")
            tgb.button("Close", on_action=close_dialog)

# Running the GUI
if __name__ == "__main__":
    gui = Gui(page=page)
    gui.run(dark_mode=True, title="Taipy Popup Table v4.0.0dev2")