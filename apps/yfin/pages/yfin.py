"""
@author: Youwei Zheng
@target: yfinance table page
@update: 2024.08.26
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
df_pcs = process_yfin(df)
# data_df is used for your table; this is your bound variable
# it is defined in the main.py so this variable is a global variable
# you could or should define it in yfin.py
data_df = df_pcs

# ------------------------------
# on_add
# ------------------------------

def add_row(state):
    empty_row = pd.DataFrame(
        [[None for _ in state.df_pcs.columns]], columns=state.df_pcs.columns
    )
    state.data_df = pd.concat([empty_row, state.df_pcs], axis=0, ignore_index=True)

    notify(state, "S", f"Added one row")

def edit_cell(state):
    pass

# ------------------------------
# Create page
# ------------------------------

with tgb.Page() as page_yfin:
    # Create title
    tgb.toggle(theme=True)
    tgb.text("# Table Data from yfinance ", mode="md", class_name="text-center pb1")

    # Create table
    tgb.table(
        "{data_df}", 
        editable=True, 
        on_add=add_row,
        on_edit=edit_cell,
        on_delete=False
    )
