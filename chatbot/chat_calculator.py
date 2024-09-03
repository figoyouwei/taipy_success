# Copyright 2021-2024 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
# -----------------------------------------------------------------------------------------
# To execute this script, make sure that the taipy-gui package is installed in your
# Python environment and run:
#     python <script>
# -----------------------------------------------------------------------------------------
# Human-computer dialog UI based on the chat control.
# -----------------------------------------------------------------------------------------

from math import cos, pi, sin, sqrt, tan  # noqa: F401

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