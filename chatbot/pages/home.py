"""
@author: Youwei Zheng
@target: sidebar page with toggle
@update: 2024.12.17
"""

import taipy.gui.builder as tgb
from taipy.gui import navigate, notify

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

from pages.chat import create_initial_chat_session
from models.chat import ChatSession
from models.chat import SessionCollection

import taipy.enterprise.gui as tp_enterprise

# ------------------------------
# logout
# ------------------------------

def on_logout(state):
    try:        
        # Store the user_session_id for logging
        old_session_id = state.user_session_id
        
        # Reset auth-related state variables
        state.username = None
        state.password = None
        state.credentials = None
        state.login_dialog = True
        state.sidebar_switch = False
        
        # Reset all chat-related variables to None first
        state.chat_session = None
        state.messages = []
        state.selected_session = None
        state.session_collection = None
        state.sessions = []
        state.user_session_id = ""
        
        # update partial sidebar
        toggle_partial_sidebar(state)

        # Logout from taipy enterprise
        tp_enterprise.logout(state)
        
        print(f"Logged out user: {old_session_id}")
        notify(state, "success", "Logged out successfully")
        
        # Navigate back to login page
        navigate(state, "login", force=True)
    except Exception as e:
        notify(state, "error", f"Logout failed: {e}")
        print(f"Logout exception: {e}")

# ------------------------------
# home page
# ------------------------------

def toggle_partial_sidebar(state):
    print("home.py: toggle_partial_sidebar")
    print("state.user_session_id: ", state.user_session_id)
    print("state.sidebar_switch: ", state.sidebar_switch)

    if state.sidebar_switch:
        with tgb.Page() as sidebar:
            with tgb.layout(columns="1 11", columns__mobile="1"):
                with tgb.part(class_name="sidebar"):
                    tgb.toggle("{sidebar_switch}", on_change=toggle_partial_sidebar)
                tgb.part(
                    class_name="p2 align-item-bottom table",
                    partial="{partial_chat}",
                )
    else:
        with tgb.Page() as sidebar:
            with tgb.layout(columns="1 3", columns__mobile="1"):
                # NOTE: sidebar class
                with tgb.part(class_name="sidebar"):
                    with tgb.layout(columns="1 2 1"):
                        with tgb.part():
                            tgb.toggle("{sidebar_switch}", on_change=toggle_partial_sidebar)
                        with tgb.part():
                            tgb.text("")
                        with tgb.part():
                            tgb.button(
                                "Logout", class_name="fullwidth", on_action=on_logout
                            )

                    # NOTE: profile image
                    tgb.image(content="icons/icon_guest.png", class_name="profile_image")

                    # NOTE: sidebar titles
                    tgb.text(
                        "#### {user_session_id}", class_name="text-center profile_name", mode="md"
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

                tgb.part(
                    class_name="p2 align-item-bottom table", partial="{partial_chat}"
                )

    state.partial_sidebar.update_content(state, sidebar)

with tgb.Page() as page_home:
    tgb.part(partial="{partial_sidebar}")