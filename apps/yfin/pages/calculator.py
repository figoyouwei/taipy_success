'''
@author: Youwei Zheng
@target: Index Calculator
@update: 2024.09.03
'''

import taipy.gui.builder as tgb
from taipy.gui import notify

from apps.yfin.models.calculator import Level
from apps.yfin.turing import compute_points

def filter_reset(state):
    # notify and refresh state
    state.levels = Level()
    
    notify(state, "info", "Filters has been reset.")
    filter_refresh(state)
    
def filter_refresh(state):
    state.levels = Level(
        starting_level=state.levels.starting_level,
        target_level=state.levels.target_level
    )

    # Turing
    state.points = compute_points(state.levels)
    notify(state, "info", "Filters applied and data updated.")


# ------------------------------
# Init page instances
# ------------------------------

# NOTE: to verify the local variables
levels = Level()
points = compute_points(levels)

# ------------------------------
# Creating page object
# ------------------------------
        
with tgb.Page() as page:
    # title line
    tgb.toggle(theme=True)
    tgb.text("### Taipy Calculator", mode="md", class_name="text-center pb1")

    # reset button
    with tgb.layout("1", class_name="pb1"):                
        with tgb.part(class_name="text-center"):
            # reset button
            tgb.button("RESET", on_action=filter_reset)
        
    # indicators
    with tgb.layout("1 1", class_name="pb1"):
        with tgb.part(class_name="card"):
            tgb.text("## Points Net", mode="md", class_name="text-center")
            tgb.text("## {points.points_net}", mode="md", class_name="text-center")
        with tgb.part(class_name="card"):
            tgb.text("## Points Pct", mode="md", class_name="text-center")
            tgb.text("## {points.points_pct}%", mode="md", class_name="text-center")

    # input fields
    with tgb.layout("1 1", class_name="pb1"):
        # Starting level
        with tgb.part(class_name="card text-center"):
            tgb.number(
                label="Starting level",
                value="{levels.starting_level}",
                on_change=filter_refresh
            )
        
        # Target level
        with tgb.part(class_name="card text-center"):
            tgb.number(
                label="Target level",
                value="{levels.target_level}",
                on_change=filter_refresh
            )

    # footer
    tgb.text("Developed by CR7", mode="md", class_name="text-center pb1")               
