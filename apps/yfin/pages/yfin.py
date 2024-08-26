'''
@author: Youwei Zheng
@target: yfinance table page
@update: 2024.08.26
'''

from taipy.gui import notify
import taipy.gui.builder as tgb
import pandas as pd

# ------------------------------
# on_add
# ------------------------------

def add_row(state):
    empty_row = pd.DataFrame(
        [[None for _ in state.df_pcs.columns]], columns=state.df_pcs.columns
    )
    state.df_pcs = pd.concat([empty_row, state.df_pcs], axis=0, ignore_index=True)

    notify(state, "S", f"Added one row")

# ------------------------------
# Create page
# ------------------------------

def create_page(data_df=None) -> pd.DataFrame:
    """Integrate pages and data.

    Returns:
        _type_: _description_
    """
    with tgb.Page() as page:
        # Create title
        tgb.toggle(theme=True)
        tgb.text("# Table Data from yfinance ", mode="md", class_name="text-center pb1")

        # Create table
        tgb.table(
            "{data_df}",
            on_add=add_row
        )    

    return page
