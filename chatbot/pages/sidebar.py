"""
@author: Youwei Zheng
@target: sidebar page
@update: 2024.09.05
"""

import taipy.gui.builder as tgb

from pages.chat import reset_chat
from pages.chat import page_chat

# ------------------------------
# Functions
# ------------------------------

def selector_adapter(item: list):
    """
    Converts element of history_conversations to (id and displayed string)?

    Args:
        item: element of history_conversations

    Returns:
        id and displayed string
    """
    print("item", item, type(item))
    conversation = item[1]
    last_message_info = conversation[len(conversation) - 1]
    last_message = last_message_info[1]
    return (str(item[0]), last_message[:50] + "...")


def select_conv(state, var_name: str, value) -> None:
    """
    Display the messages of selected conversation from history_conversations in tgb.chat()

    Args:
        state: The current state of the app.
        var_name: "selected_conv"
        value: [[id, conversation]]
    """
    state.selected_conversation = state.selected_conv[1]
    state.partial_chat.update_content(state, page_chat)

# ------------------------------
# Create page
# ------------------------------

from pages.chat import selected_conversation
from pages.chat import history_conversations

with tgb.Page() as page_sidebar:
    # NOTE: fixed width 300px
    with tgb.layout("300px 1", columns__mobile="1"):
        # NOTE: sidebar class
        with tgb.part(class_name="sidebar"):
            # sidebar title
            tgb.text("## Chatbot Demo", class_name="text-center", mode="md")
            # sidebar button
            tgb.button(
                "New Conversation",
                on_action=reset_chat,
                class_name="fullwidth plain",
            )

            tgb.text("### Previous activities", mode="md", class_name="h5 mt2 mb-half")
            tgb.selector(
                "{selected_conversation}",
                lov="{history_conversations}",
                on_change=select_conv,
                adapter=selector_adapter,
                # NOTE: css identifier
                id="past_prompts_list",
                class_name="past_prompts_list",
            )

        # NOTE: partial chat
        tgb.part(class_name="p2 align-item-bottom table", partial="{partial_chat}")
