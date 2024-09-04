"""
@author: Youwei Zheng
@target: sidebar page
@update: 2024.09.04
"""

import taipy.gui.builder as tgb

from pages.chat import reset_chat

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as page:
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

            # tgb.text("### Previous activities", mode="md", class_name="h5 mt2 mb-half")
            # tgb.selector(
            #     "{selected_conv}",
            #     lov="{past_conversations}",
            #     id="past_prompts_list",
            #     on_change=select_conv,
            #     adapter=selector_adapter,
            #     class_name="past_prompts_list",
            # )

        # NOTE: partial chat
        tgb.part(class_name="p2 align-item-bottom table", partial="{partial_chat}")
