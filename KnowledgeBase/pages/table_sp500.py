'''
@author: Youwei Zheng
@target: S&P 500 Table
@source: https://docs.taipy.io/en/develop/tutorials/visuals/2_using_tables/
@update: 2024.08.14
'''

import taipy.gui.builder as tgb
from taipy.gui import Gui, Markdown, notify
import pandas as pd

# ------------------------------
# food df
# ------------------------------

food_df = pd.DataFrame({
    "Meal": ["Lunch", "Dinner", "Lunch", "Lunch", "Breakfast", "Breakfast", "Lunch", "Dinner"],
    "Category": ["Food", "Food", "Drink", "Food", "Food", "Drink", "Dessert", "Dessert"],
    "Name": ["Burger", "Pizza", "Soda", "Salad", "Pasta", "Water", "Ice Cream", "Cake"],
    "Calories": [300, 400, 150, 200, 500, 0, 400, 500],
})

# ------------------------------
# sp500 df
# ------------------------------
    
def create_page(df_table: str):
    with tgb.Page() as page:
        tgb.text("# S&P 500 Daily Data, Not Future", mode="md", class_name="text-center pb1")

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

from scenarios.sp500 import (
    download_data_sp500, 
    process_data_sp500, 
    create_scenario
)

import taipy as tp

if __name__ == "__main__":

    # Run data
    data_input = download_data_sp500()
    data_input

    # Creation of the scenario and execution
    scenario = create_scenario(
        tool2call=process_data_sp500,
        node_input_name="data_in",
        node_output_name="data_out",
        task_id="task",
        scenario_id="scenario"
    )
    
    scenario.data_in.write(data_input)
    tp.submit(scenario)

    df_sp500 = scenario.data_out.read()
    
    # Create and run
    df_table = "{df_sp500}"
    page = create_page(df_table=df_table)
    Gui(page=page).run(
        debug=True
    )