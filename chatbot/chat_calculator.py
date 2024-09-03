"""
@author: Youwei Zheng
@target: Issue #10
@update: 2024.09.03
"""

import taipy.gui.builder as tgb
from taipy.gui import Gui

# The user interacts with the Python interpreter
users = ["Human", "Result"]
messages: list[tuple[str, str, str]] = []

# ------------------------------
# Action function
# ------------------------------

def evaluate(state, var_name: str, payload: dict):
    # Retrieve the callback parameters
    (_, _, expression, sender_id) = payload.get("args", [])
    print(sender_id)
    print(expression)
 
    # Add the input content as a sent message
    messages.append((f"{len(messages)}", expression, sender_id))
    print(messages)
 
    # Default message used if evaluation fails
    result = "Invalid expression"
    try:
        # Evaluate the expression and store the result
        result = f"{eval(expression)}"
    except Exception:
        pass
 
    # Add the result as an incoming message
    messages.append((f"{len(messages)}", result, users[1]))
    print(messages)

    state.messages = messages

# ------------------------------
# Create page object
# ------------------------------

with tgb.Page() as page:
    tgb.chat(
        "{messages}", 
        users=users, 
        on_action=evaluate, 
        sender_id="{users[0]}",
        # * In this case, always Human
    )

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Starting calculator...")
    Gui(page).run()