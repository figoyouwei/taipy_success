'''
@author: Youwei Zheng
@target: Taipy GUI
@update: 2024.07.25
'''

import taipy.gui.builder as tgb
from taipy.gui import notify

from turing import levels

def filter_reset(state):
    # notify and refresh state
    state.starting_level = 565.16
    state.target_level = 540.00
    
    notify(state, "info", "Filters has been reset.")
    filter_refresh(state)
    
def filter_refresh(state):
    print("Entering on_filter()")

    # Turing
    (
        state.points_net,
        state.points_pct
    ) = levels(
        state.starting_level,
        state.target_level
    )

    notify(state, "info", "Filters applied and data updated.")

def setup_gui(filter_refresh, filter_reset):
        
    with tgb.Page() as page:
        # title line
        tgb.toggle(theme=True)
        tgb.text("# Taipy Deployment on Heroku", mode="md", class_name="text-center pb1")

        # reset button
        with tgb.layout("1", class_name="pb1"):                
            with tgb.part(class_name="text-center"):
                # reset button
                tgb.button("RESET", on_action=filter_reset)
            
        # indicators
        with tgb.layout("1 1", class_name="pb1"):
            with tgb.part(class_name="card"):
                tgb.text("## Points Net", mode="md", class_name="text-center")
                tgb.text("## {points_net}", mode="md", class_name="text-center")
            with tgb.part(class_name="card"):
                tgb.text("## Points Pct", mode="md", class_name="text-center")
                tgb.text("## {points_pct}%", mode="md", class_name="text-center")

        # input fields
        with tgb.layout("1 1", class_name="pb1"):
            # Starting level
            with tgb.part(class_name="card text-center"):
                tgb.input(
                    label="Starting level",
                    value="{starting_level}",
                    on_change=filter_refresh
                )
            
            # Target level
            with tgb.part(class_name="card text-center"):
                tgb.input(
                    label="Target level",
                    value="{target_level}",
                    on_change=filter_refresh
                )

        # footer
        tgb.text("Developed by Youwei Zheng", mode="md", class_name="text-center pb1")               
    return page
