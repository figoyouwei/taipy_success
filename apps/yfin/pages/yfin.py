"""
@author: Youwei Zheng
@target: yfinance table page
@update: 2024.08.29
"""

from datetime import datetime

from taipy.gui import notify
import taipy.gui.builder as tgb
import pandas as pd

from tools import download_yfin, process_yfin

# ------------------------------
# on_init
# ------------------------------

current_date = datetime.now().strftime("%Y-%m-%d")
args_in = (
    "^SPX",
    "1d",
    "2024-08-01",
    current_date,
)
df = download_yfin(args_in)
data_table = process_yfin(df)

# data_df is used for your table; this is your bound variable
# it is defined in the main.py so this variable is a global variable
# you could or should define it in yfin.py

# ------------------------------
# on_add
# ------------------------------

def on_add(state):
    empty_row = pd.DataFrame(
        [[None for _ in state.data_table.columns]], columns=state.data_table.columns
    )
    state.data_table = pd.concat([empty_row, state.data_table], axis=0, ignore_index=True)

    notify(state, "S", f"Added one row")

def on_edit(state, var_name, payload):
    index = payload["index"]  # row index
    col = payload["col"]  # column name
    value = payload["value"]  # new value cast to the column type
    user_value = payload["user_value"]  # new value as entered by the user

    old_value = state.data_table.loc[index, col]
    data_table = state.data_table.copy()
    data_table.loc[index, col] = value
    state.data_table = data_table
    notify(
        state=state,
        notification_type="I",
        message=f"Edited value from '{old_value}' to '{value}'. (index '{index}', column '{col}')",
    )

def on_delete(state, var_name, payload):
    index = payload["index"]  # row index

    state.data_table = state.data_table.drop(index=index)
    notify(state, "E", f"Deleted row at index '{index}'")

# ------------------------------
# Create page
# ------------------------------

table_mode = False

def toggle_mode(state):
    print("Before toggle", state.table_mode)
    if state.table_mode == False:
        state.table_mode = True
    else:
        state.table_mode = False
    print("After toggle", state.table_mode)
        
    notify(state, "I", f"Toggle table mode")


with tgb.Page() as page_yfin:
    # Create title
    tgb.toggle(theme=True)
    tgb.text("# Table Data from yfinance ", mode="md", class_name="text-center pb1")

    with tgb.layout("1", class_name="pb1 text-center"):
        tgb.text("Editing Mode: ", mode="md", class_name="text-center")
        tgb.toggle(value="{table_mode}")

        with tgb.part(render="{table_mode == False}"):
            tgb.table(
                "{data_table}",
                editable=False,
                on_add=on_add,
                on_edit=on_edit,
                on_delete=on_delete
            )

        with tgb.part(render="{table_mode}"):
            tgb.table(
                "{data_table}",
                editable=True,
                on_add=on_add,
                on_edit=on_edit,
                on_delete=on_delete
            )
            