"""
@author: Youwei Zheng
@target: sidebar page
@update: 2024.09.06
"""

import taipy.gui.builder as tgb
from models.chat import ChatSession

# ------------------------------
# Import functions
# ------------------------------

from pages.chat import reset_session
from pages.chat import select_session
from pages.chat import selector_adapter

# ------------------------------
# Import state variables
# ------------------------------

from pages.chat import selected_session
from pages.chat import sessions

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as page_home:
    # NOTE: fixed width 300px or 1 3
    # with tgb.layout(columns="300px 1", columns__mobile="1"):
    with tgb.layout(columns="1 3", columns__mobile="1"):
        # NOTE: sidebar class
        with tgb.part(class_name="sidebar"):
            # sidebar title
            tgb.text("## Chatbot Demo", class_name="text-center", mode="md")

            # NOTE: reset part
            tgb.button(
                "New Session",
                on_action=reset_session,
                class_name="fullwidth plain",
            )

            # NOTE: selector part
            tgb.text("### Previous activities", mode="md", class_name="h5 mt2 mb-half text-center")
            tgb.selector(
                value="{selected_session}",
                lov="{sessions}",
                on_change=select_session,
                # NOTE: displayed text of selector item
                type=ChatSession,
                adapter=selector_adapter,
                # NOTE: css identifier
                id="past_prompts_list",
                class_name="past_prompts_list",
            )

        # NOTE: partial chat
        tgb.part(class_name="p2 align-item-bottom table", partial="{partial_chat}")
