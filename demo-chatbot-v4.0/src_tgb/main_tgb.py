import os
import sys

from taipy.gui import Gui, notify, Icon, navigate
import openai
import taipy.gui.builder as tgb
from openai_utils import request
from stateclass import State
from typing import List, Optional


# Global OpenAI client
client: openai.Client = None

# Initialize conversation context
initial_context: str = (
    "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?"
)
context: str = initial_context
conversation: List[List[str]] = [
    ["1", "Who are you?", "Human"],
    ["2", "Hi! I am GPT-4. How can I help you today?", "AI"],
]

users: List[List[str]] = [
    ["Human", Icon("/images/human_icon.png", "Human.png")],
    ["AI", Icon("/images/ai_icon.png", "AI.png")],
]

selected_conv: Optional[List[List[str]]] = None

past_conversations: List[List[List[str]]] = []
id = 0


def on_init(state: State) -> None:
    """
    Initialize the app.

    Args:
        - state: The current state of the app.
    """
    state.context = initial_context
    state.conversation = conversation.copy()
    state.past_conversations = []
    state.selected_conv = None


def update_context(state: State, current_user_message) -> str:
    """
    Update the context with the user's message and the AI's response.

    Args:
        - state: The current state of the app.
    """
    state.context += f"Human: {current_user_message}\n\nAI:"
    answer = request(state, state.context).replace("\n", "")
    state.context += answer
    return answer


def send_message(state: State, var_name: str, payload: dict = None) -> None:
    """
    Send the user's message to the API and update the context.

    Args:
        - state: The current state of the app.
    """
    if payload:
        args = payload.get("args", [])
        current_user_message = args[2]
        sender = args[3]

    notify(state, "info", "Sending message...")
    answer = update_context(state, current_user_message)
    state.conversation += [
        [
            f"{len(state.conversation) + 1}",
            current_user_message,
            sender,
        ]
    ]

    state.conversation += [[f"{len(state.conversation) + 1}", answer, "AI"]]
    notify(state, "success", "Response received!")


# Trigger state update


def reset_chat(state: State) -> None:
    """
    Reset the chat by clearing the conversation.

    Args:
        - state: The current state of the app.
    """
    if len(state.conversation) < 3:
        notify(state, "warning", "No conversation to reset")
        return
    state.past_conversations += [(len(state.past_conversations), state.conversation)]
    state.conversation = conversation.copy()
    state.context = initial_context
    state.chat.update_content(state, build_chat())


def selector_adapter(item: list):
    """
    Converts element of past_conversations to id and displayed string

    Args:
        item: element of past_conversations

    Returns:
        id and displayed string
    """
    print("item", item, type(item))
    conversation = item[1]
    last_message_info = conversation[len(conversation) - 1]
    last_message = last_message_info[1]
    return (str(item[0]), last_message[:50] + "...")


def select_conv(state: State, var_name: str, value) -> None:
    """
    Selects conversation from past_conversations

    Args:
        state: The current state of the app.
        var_name: "selected_conv"
        value: [[id, conversation]]
    """
    state.conversation = state.selected_conv[1]
    state.context = initial_context
    for i in range(2, len(state.conversation), 2):
        state.context += f"Human: {state.conversation[i][1]}\n\nAI:"
        state.context += state.conversation[i + 1][1]
    state.chat.update_content(state, build_chat())


def build_chat():
    with tgb.Page() as chat:
        # Doc for chat control: https://docs.taipy.io/en/develop/manuals/userman/gui/viselements/generic/chat/
        tgb.chat(
            "{conversation}", users=users, on_action=send_message, sender_id="Human"
        )
    return chat


# Building the layout
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


# Main entry point
if __name__ == "__main__":
    if "OPENAI_API_KEY" in os.environ:
        api_key = os.environ["OPENAI_API_KEY"]
    elif len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = None
        # raise ValueError(
        #     "Please provide the OpenAI API key as an environment variable OPENAI_API_KEY or as a command line argument."
        # )

    client = None  # openai.Client(api_key=api_key)

    gui = Gui(page)
    chat = gui.add_partial(build_chat())
    gui.run(dark_mode=True, title="💬 Taipy Chat")
