'''
@author: Youwei Zheng
@target: Practice with Django users
@update: 2024.10.25
'''

import os
import pandas as pd
from taipy.gui import Gui, State, navigate, notify
import taipy.gui.builder as tgb
from taipy.core.config import Config
from taipy.auth import hash_taipy_password, AnyOf, Credentials
import taipy.enterprise.gui as tp_enterprise
from tools import load_data_from_postgres  # Import the function from tools.py
import hashlib
import base64
from django.conf import settings
from django.contrib.auth.hashers import check_password

# Configure Django settings
if not settings.configured:
    settings.configure(
        PASSWORD_HASHERS=[
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        ],
        SECRET_KEY='a-secret-key-for-django',
    )

os.environ["TAIPY_AUTH_HASH"] = "taipy"

username = None
credentials = None

# Load user data from the database
user_query = "SELECT username, is_superuser, password FROM auth_user"
user_df = load_data_from_postgres(user_query)
print(user_df)

if user_df is not None:
    passwords = {row['username']: row['password'] for row in user_df.to_dicts()}
    is_superuser = {row['username']: row['is_superuser'] for row in user_df.to_dicts()}
else:
    print("Failed to load user data from the database. Using default values.")
    passwords = {
        "florian": "hashed_password_for_florian",
        "alex": "hashed_password_for_alex",
    }
    is_superuser = {
        "florian": True,
        "alex": False,
    }

# Custom authenticator function
def django_authenticator(username, password):
    if username in passwords:
        stored_hash = passwords[username]
        result = check_password(password, stored_hash)
        print(f"Authentication attempt for {username}: {'Success' if result else 'Failure'}")
        return result
    print(f"Username {username} not found in passwords dictionary")
    return False

# Configure Taipy authentication with custom authenticator
Config.configure_authentication("taipy", authenticator=django_authenticator)

is_admin = lambda credentials: credentials.properties.get("is_superuser", False) if credentials else False

def custom_password_verify(plain_password, hashed_password):
    return check_password(plain_password, hashed_password)

# NOTE: overwrite default login function?
def on_login(state: State, id, login_args):
    state.username, password = login_args["args"][:2]
    try:
        if django_authenticator(state.username, password):
            state.credentials = tp_enterprise.login(state, state.username, hash_taipy_password(password))
            state.is_admin = is_superuser.get(state.username, False)  # Set is_admin based on the user
            notify(state, "success", f"Logged in as {state.username}")
            navigate(state, "data_page")
        else:
            raise Exception("Invalid username or password")
    except Exception as e:
        notify(state, "error", f"Login failed: {e}")
        print(f"Login exception: {e}")
        state.username = None
        state.credentials = None
        state.is_admin = False
        navigate(state, "login_page")

def go_to_login(state: State):
    navigate(state, "login_page", force=True)


root_page = ""

# Update the data loading for the table
data_query = "SELECT * FROM datei_ppi LIMIT 5"  # Adjust this query as needed
data = load_data_from_postgres(data_query)
if data is None:
    data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

with tgb.Page() as root_page:
    tgb.button("Account", on_action=go_to_login, class_name="login_button plain")

with tgb.Page() as login_page:
    tgb.login("Welcome to Taipy!")

with tgb.Page() as data_page:
    with tgb.part(render="{username is not None}"):
        tgb.text(value="# Welcome to Taipy, {username}", mode="md")
    with tgb.part(render="{is_admin}"):  # Changed from is_admin.get_traits(credentials)
        tgb.table(data="{data}")

pages = {
    "/": root_page,
    "data_page": data_page,
    "login_page": login_page,
}

if __name__ == "__main__":
    Gui(pages=pages).run(title="Django Chart")
