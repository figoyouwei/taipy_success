'''
@author: Youwei Zheng
@target: S&P 500 Table
@source: https://docs.taipy.io/en/develop/tutorials/visuals/2_using_tables/
@update: 2024.08.14
'''

import taipy.gui.builder as tgb
from taipy.gui import Gui, notify
import pandas as pd

# ------------------------------
# stock df
# ------------------------------
    
def create_page(df_table: str):
    with tgb.Page() as page:
        tgb.text("# US Stock Daily Index, Not Future", mode="md", class_name="text-center pb1")

        tgb.table(
            df_table,
            class_name="rows-bordered",
            # filter=True,
            # on_edit=food_df_on_edit,
            # on_delete=food_df_on_delete,
            # on_add=food_df_on_add,
            # group_by__Category=True,
            # apply__Calories="sum",
        )
        
    return page

# ------------------------------
# Main app
# ------------------------------

from app.tools.yfin import (
    download_yfin, 
    process_data_yfin, 
    create_scenario
)

import taipy as tp

if __name__ == "__main__":
    # Run data
    symbol = '^SPX'
    data_input = download_yfin(ticker_symbol=symbol)
    data_input

    # Creation of the scenario and execution
    scenario = create_scenario(
        tool2call=process_data_yfin,
        node_input_name="data_in",
        node_output_name="data_out",
        task_id="task",
        scenario_id="scenario"
    )
    
    scenario.data_in.write(data_input)
    tp.submit(scenario)

    df_yfin = scenario.data_out.read()
    
    # Create and run
    df_table = "{df_yfin}"
    page = create_page(df_table=df_table)
    Gui(page=page).run(
        debug=True
    )