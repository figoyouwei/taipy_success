"""
@author: Youwei Zheng
@target: sidebar page
@update: 2024.09.05
"""

import taipy.gui.builder as tgb

# ------------------------------
# Import functions
# ------------------------------

from pages.chat import reset_chat
from pages.chat import select_session
from pages.chat import selector_adapter

# ------------------------------
# Import state variables
# ------------------------------

from pages.chat import selected_session
from pages.chat import chat_sessions

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as page_sidebar:
    # NOTE: fixed width 300px
    with tgb.layout("300px 1", columns__mobile="1"):
        # NOTE: sidebar class
        with tgb.part(class_name="sidebar"):
            # sidebar title
            tgb.text("## Chatbot Demo", class_name="text-center", mode="md")
            # sidebar button
            tgb.button(
                "New Session",
                on_action=reset_chat,
                class_name="fullwidth plain",
            )

            tgb.text("### Previous activities", mode="md", class_name="h5 mt2 mb-half")
            tgb.selector(
                "{selected_session}",
                lov="{chat_sessions}",
                on_change=select_session,
                # NOTE: displayed text of selector item
                adapter=selector_adapter,
                # NOTE: css identifier
                id="past_prompts_list",
                class_name="past_prompts_list",
            )

        # NOTE: partial chat
        tgb.part(class_name="p2 align-item-bottom table", partial="{partial_chat}")
