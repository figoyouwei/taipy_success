"""
@author: Youwei Zheng
@target: query page
@update: 2024.12.03
"""

from taipy.gui import notify
import taipy.gui.builder as tgb

# ------------------------------
# Import functions
# ------------------------------

from services.query_table import query_master

# ------------------------------
# Create page
# ------------------------------

def make_call(state):
    print("Make call")
    notify(state, "i", "We are preparing your answer...")
    print("state.user_query: ", state.user_query)
    
    # Clear existing results first
    state.query_result = None
    
    # Get new results
    result = query_master(state.user_query)
    
    # Update state with new results
    state.query_result = result
    print(state.query_result)
    notify(state, "i", "We have delivered your answer.")


with tgb.Page() as page_home:
    tgb.toggle(theme=True)
    tgb.text("# 对话即数据应用", mode="md", class_name="text-center pb1")

    # Input field
    with tgb.layout("1", class_name="text-center pb1"):
        with tgb.part(class_name="card"):
            tgb.input(
                label="Question",
                value="{user_query}",
                class_name="question_field",
                hover_text="What you want to know about our data?"                
            )

    # Input button
    with tgb.layout("1", class_name="text-center pb1"):
        with tgb.part():
            tgb.button(
                "Ask",
                on_action=make_call,
                class_name="text-center ask_button"
            )

    # display full table
    tgb.table(
        "{query_result}",
        class_name="result-table",
        height="400px"  # Optional: sets a fixed height for better visibility
    )

