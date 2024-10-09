'''
@author: Youwei Zheng
@target: Income Calculator
@update: 2024.09.30
'''

import taipy.gui.builder as tgb
from taipy.gui import notify

from turing import compute_income

def filter_reset(state):
    # notify and refresh state
    state.rate_per_hour = rate_per_hour
    state.hours_per_week = hours_per_week
    state.weeks_per_year = weeks_per_year
    
    notify(state, "info", "Filters has been reset.")
    filter_refresh(state)
    
def filter_refresh(state):
    # Turing
    (state.income_weekly, state.income_yearly) = compute_income(
        rph=state.rate_per_hour,
        hours=state.hours_per_week,
        weeks=state.weeks_per_year
    )
    notify(state, "info", "Filters applied and data updated.")

# ------------------------------
# Init page instances
# ------------------------------

# NOTE: default variables
rate_per_hour:int = 65
hours_per_week:int = 12
weeks_per_year:int = 48

income_weekly = rate_per_hour * hours_per_week
income_yearly = income_weekly * weeks_per_year

# ------------------------------
# Creating page object
# ------------------------------
        
layout_columns = "2 8"  # Define your layout columns ratio
from pages.sidebar import sidebar_partial

with tgb.Page() as page:
    with tgb.layout(columns=layout_columns):
        with tgb.part("sidebar"):
            sidebar_partial()  # Render the sidebar content
        
        with tgb.part("math"):
            tgb.navbar()  # Render the navbar
            tgb.html("h1", "Freelancer Math")

            # reset button
            with tgb.layout("1", class_name="pb1"):                
                with tgb.part(class_name="text-left"):
                    # reset button
                    tgb.button("RESET", on_action=filter_reset)
                
            # indicators
            with tgb.layout("1 1", class_name="pb1"):
                with tgb.part(class_name="card"):
                    tgb.text("## Income Weekly", mode="md", class_name="text-center")
                    tgb.text("## ${income_weekly}", mode="md", class_name="text-center")
                with tgb.part(class_name="card"):
                    tgb.text("## Income Yearly", mode="md", class_name="text-center")
                    tgb.text("## ${income_yearly}", mode="md", class_name="text-center")

            # input fields
            with tgb.layout("1 1 1", class_name="pb1"):
                # Rate per hour
                with tgb.part(class_name="card text-center"):
                    tgb.number(
                        label="Rate per hour",
                        value="{rate_per_hour}",
                        on_change=filter_refresh
                    )

                # Hours per week
                with tgb.part(class_name="card text-center"):
                    tgb.number(
                        label="Hours per week",
                        value="{hours_per_week}",
                        on_change=filter_refresh
                    )
                
                # Weeks per year
                with tgb.part(class_name="card text-center"):
                    tgb.number(
                        label="Weeks per year",
                        value="{weeks_per_year}",
                        on_change=filter_refresh
                    )
 
# with tgb.Page() as page:
#     # title line
#     tgb.toggle(theme=True)
#     tgb.text("### Data Freelancer Math", mode="md", class_name="text-center pb1")

#     # reset button
#     with tgb.layout("1", class_name="pb1"):                
#         with tgb.part(class_name="text-center"):
#             # reset button
#             tgb.button("RESET", on_action=filter_reset)
        
#     # indicators
#     with tgb.layout("1 1", class_name="pb1"):
#         with tgb.part(class_name="card"):
#             tgb.text("## Income Weekly", mode="md", class_name="text-center")
#             tgb.text("## ${income_weekly}", mode="md", class_name="text-center")
#         with tgb.part(class_name="card"):
#             tgb.text("## Income Yearly", mode="md", class_name="text-center")
#             tgb.text("## ${income_yearly}", mode="md", class_name="text-center")

#     # input fields
#     with tgb.layout("1 1 1", class_name="pb1"):
#         # Rate per hour
#         with tgb.part(class_name="card text-center"):
#             tgb.number(
#                 label="Rate per hour",
#                 value="{rate_per_hour}",
#                 on_change=filter_refresh
#             )

#         # Hours per week
#         with tgb.part(class_name="card text-center"):
#             tgb.number(
#                 label="Hours per week",
#                 value="{hours_per_week}",
#                 on_change=filter_refresh
#             )
        
#         # Weeks per year
#         with tgb.part(class_name="card text-center"):
#             tgb.number(
#                 label="Weeks per year",
#                 value="{weeks_per_year}",
#                 on_change=filter_refresh
#             )
