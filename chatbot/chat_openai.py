"""
@author: Youwei Zheng
@target: Chat with openai
@update: 2024.09.03
"""

import taipy.gui.builder as tgb
from taipy.gui import Gui, notify, Icon

from typing import List

# The user interacts with the Python interpreter only via css to change icon size
users: List[List[str]] = [
    ["Human", Icon("/icons/icon_hm.png")],
    ["AI", Icon("/icons/icon_ai.png")],
]

messages: list[tuple[str, str, str]] = []

# ------------------------------
# Action function
# ------------------------------

from tools.chatcpl import chat_tongyi

def evaluate(state, var_name: str, payload: dict):
    """_summary_

    Args:
        state (_type_): _description_
        var_name (str): not sure of its function
        payload (dict): _description_
    """
    notify(state, "I", f"We are preparing your answer...")

    # Retrieve the callback parameters
    (_, _, message_hm, sender_id) = payload.get("args", [])
 
    # Add the input content as a sent message
    messages.append((f"{len(messages)}", message_hm, sender_id))
    print(messages)
 
    # Default message used if evaluation fails
    result = "Invalid expression"
    try:
        # Evaluate the expression and store the result
        result = chat_tongyi(message_hm)
    except Exception:
        pass
 
    # Add the result as an incoming message
    messages.append((f"{len(messages)}", result, "AI"))
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
        sender_id="Human",
        # * In this case, always Human
    )

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    print("Starting chatting with openai...")
    Gui(page).run()