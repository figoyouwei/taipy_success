import os
import pandas as pd

from taipy.gui import Gui, State, navigate, notify
import taipy.gui.builder as tgb
from taipy.core.config import Config

from taipy.auth import hash_taipy_password, AnyOf, Credentials, Authenticator
import taipy.enterprise.gui as tp_enterprise

os.environ["TAIPY_AUTH_HASH"] = "taipy"

username = None
credentials = None

user_django = {
    "florian": "flower", # TODO: shall be django hash password
    "alex": "alex24", # TODO: shall be django hash password
}

roles = {
    "florian": ["admin", "staff"],
    "alex": ["staff"],
}

Config.configure_authentication("taipy", passwords=user_django, roles=roles)

def django_authenticator(username, password):
    # TODO: implement django authenticator
    pass

# NOTE: overwrite tgb.login()?
def on_login(state: State, id, login_args):
    state.username, password = login_args["args"][:2]
    try:
        state.credentials = tp_enterprise.login(state, state.username, password, authenticator=django_authenticator)
        notify(state, "success", f"Logged in as {state.username}...")
        navigate(state, "data_page", force=True)
    except Exception as e:
        notify(state, "error", f"Login failed: {e}")
        print(f"Login exception: {e}")
        navigate(state, "login_page", force=True)


def go_to_login(state: State):
    navigate(state, "login_page", force=True)


root_page = ""

data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

with tgb.Page() as root_page:
    tgb.button("Account", on_action=go_to_login, class_name="login_button plain")

with tgb.Page() as login_page:
    tgb.login("Welcome to Taipy!")

with tgb.Page() as data_page:
    with tgb.part(render="{username is not None}"):
        tgb.text(value="# Welcome to Taipy, {username}", mode="md")
    with tgb.part(render="{is_admin.get_traits(credentials)}"):
        tgb.table(data="{data}")

pages = {
    "/": root_page,
    "data_page": data_page,
    "login_page": login_page,
}

if __name__ == "__main__":
    Gui(pages=pages).run(title="Dynamic chart")
