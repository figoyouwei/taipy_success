import os
import pandas as pd

from taipy.gui import Gui, State, navigate, notify
import taipy.gui.builder as tgb
from taipy.config import Config
from taipy.auth import hash_taipy_password, AnyOf, Credentials
import taipy.enterprise.gui as tp_enterprise

# Set environment variable for Taipy authentication
os.environ["TAIPY_AUTH_HASH"] = "taipy"

# Create default credentials state object
username = None
credentials = None

# Define user passwords (hashed for security)
passwords = {
    "florian": hash_taipy_password("flower"),
    "alex": hash_taipy_password("alex24"),
}

# Define user roles
roles = {
    "florian": ["admin", "staff"],
    "alex": ["reader"],
}

# Configure Taipy authentication
Config.configure_authentication("taipy", passwords=passwords, roles=roles)

# Create an AnyOf object to check if a user has a specific role
def has_role(role):
    return AnyOf(role, True, False)

# Example usage:
is_admin = has_role("admin")
is_reader = has_role("reader")


# Login function
def on_login(state: State, id, login_args):
    # Extract username and password from login_args
    state.username, password = login_args["args"][:2]
    # print(f"Username: {state.username}, Password: {password}")
    try:
        # Attempt to log in using Taipy Enterprise
        state.credentials = tp_enterprise.login(state, state.username, password)
        notify(state, "success", f"Logged in as {state.username}...")
        navigate(state, "Overview", force=True)
    except Exception as e:
        notify(state, "error", f"Login failed: {e}")
        print(f"Login exception: {e}")
        navigate(state, "Login", force=True)


# Function to navigate to the login page
def navigate_to_login(state: State):
    navigate(state=state, to="LoginDialog", force=True)


# Initialize root page
# root_page = ""

# Create sample data for display
data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

# Define root page
with tgb.Page() as root_page:
    tgb.button("Account", on_action=navigate_to_login, class_name="login_button plain")

# Define login page
with tgb.Page() as login_page:
    tgb.login("Welcome to Taipy!")

# Define Overview page
with tgb.Page() as Overview:
    tgb.text(value="# Welcome to Taipy, {username}", mode="md")
    # tgb.text(value="{username}")
    # Display table only if user has admin role
    with tgb.part(render="{has_role('admin')}"):
        tgb.table(data="{data}")

# Define page routing
pages = {
    "/": root_page,
    "LoginDialog": login_page,
    "Overview": Overview,
}

# Run the application
if __name__ == "__main__":
    Gui(pages=pages).run(title="Auth-based chart", reload=True)
