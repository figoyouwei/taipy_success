from taipy.gui import Gui, State
import taipy.gui.builder as tgb

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


# Build the page layout
with tgb.Page() as page:
    # Button to open the dialog
    tgb.button("Open Pop-up", on_action=open_dialog)
    
    # Dialog that will pop up when 'show_dialog' is True
    with tgb.dialog("{show_dialog}", on_action=close_dialog):
        tgb.text("{some_content}")
        tgb.button("Close", on_action=close_dialog)

# Running the GUI
if __name__ == "__main__":
    Gui(page=page, on_init=on_init).run()
