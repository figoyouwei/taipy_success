"""
@author: Youwei Zheng
@target: Whole page
@update: 2024.09.03
"""

import taipy.gui.builder as tgb

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as page:
    with tgb.layout("300px 1", columns__mobile="1"):
        with tgb.part("sidebar"):
            tgb.text("# Taipy **Chat**", mode="md")
            tgb.button(
                "New Conversation",
                on_action=reset_chat,
                class_name="fullwidth plain",
            )
            tgb.text("### Previous activities", mode="md", class_name="h5 mt2 mb-half")
            tgb.selector(
                "{selected_conv}",
                lov="{past_conversations}",
                id="past_prompts_list",
                on_change=select_conv,
                adapter=selector_adapter,
                class_name="past_prompts_list",
            )

        tgb.part("p2 align-item-bottom table", partial="{chat}")
