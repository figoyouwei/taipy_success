"""
@author: Youwei Zheng
@target: sidebar page with toggle
@update: 2024.11.11
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

# NOTE: display sidebar by default
sidebar_switch = False

def toggle_partial_sidebar(state):
    if state.sidebar_switch:
        with tgb.Page() as sidebar:
            tgb.toggle("{sidebar_switch}", on_change=toggle_partial_sidebar)
            tgb.part(class_name="p2 align-item-bottom table", partial="{partial_chat}")
    else:
        with tgb.Page() as sidebar:
            with tgb.layout(columns="1 3", columns__mobile="1"):
                # NOTE: sidebar class
                with tgb.part(class_name="sidebar"):
                    tgb.toggle("{sidebar_switch}", on_change=toggle_partial_sidebar)
                    tgb.image(content="icons/icon_hm.png", class_name="profile_image")
                    # sidebar titles
                    tgb.text(
                        "## Username", class_name="text-center profile_name", mode="md"
                        )
                    tgb.text(
                        "## Verified Name", class_name="text-center", mode="md"
                        )

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

                    # NOTE: reset part
                    tgb.button(
                        "New Session",
                        on_action=reset_session,
                        class_name="fullwidth plain",
                    )

                    # NOTE: selector part
                    tgb.text(
                        "### Previous activities",
                        mode="md",
                        class_name="h5 mt2 mb-half text-center",
                    )
                tgb.part(
                    class_name="p2 align-item-bottom table", partial="{partial_chat}"
                )

    state.partial_sidebar.update_content(state, sidebar)


with tgb.Page() as page_home:
    tgb.part(partial="{partial_sidebar}")