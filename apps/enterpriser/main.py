'''
@author: Youwei Zheng
@target: Taipy Frontend of Icebreaker app.
@update: 2024.08.26
'''

from taipy.gui import Gui
from taipy.gui import notify

import taipy.gui.builder as tgb

from ice_breaker import ice_breaker_with

# ------------------------------
# on_filter
# ------------------------------

def on_filter(state):
    try:
        # get data from tool calling
        res, data = ice_breaker_with(state.userinput)
        state.render_progress = True
        state.summary_info = res.summary
        state.facts = res.facts
        notify(state, "info", "Filters applied and data updated.")

        # partial
        add_partial_facts(state)
    except Exception as e:
        state.summary_info = "An error occurred while fetching the profile."
        notify(state, "error", f"Error: {str(e)}")

# ------------------------------
# add partial
# ------------------------------

def add_partial_facts(state):
    # update List content using partials
    with tgb.Page() as partial:
        for index, fact in enumerate(state.facts):
            tgb.text(f"{index}: {fact}", mode="md")

    state.partial_facts.update_content(state, partial)

# ------------------------------
# page creation
# ------------------------------

def create_page():
    with tgb.Page() as page:
        tgb.toggle(theme=True)
        tgb.text("# Company Profile Engine", mode="md", class_name="text-center pb1")

        # Input field
        with tgb.layout("1", class_name="text-center pb1"):
            with tgb.part(class_name="card"):
                tgb.input(
                    label="Company",
                    value="{userinput}",
                    hover_text="Please input one name"
                )

        # Input button
        with tgb.layout("1", class_name="text-center pb1"):
            with tgb.part():
                tgb.button(
                    "Display Profile", 
                    on_action=on_filter, 
                    class_name="text-center"
                )

        # progress element
        # tgb.progress("{progress_value }", render="{render_progress}")

        # Summary area
        tgb.text("{summary_info}", mode="md", class_name="text-left pb1")

        # Facts area
        tgb.part(partial="{partial_facts}")

    return page

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    # 初始化用户输入
    userinput = ""
    summary_info = ""
    facts = []

    # progress settings?
    render_progress = False
    progress_value = None

    page = create_page()
    gui = Gui(page)

    # add new partial object defined by page?
    partial_facts = gui.add_partial("")

    # run gui
    gui.run(
        title="Company Profile Engine",
        debug=True,
        use_reloader=True,
        watermark="Made by Youwei Zheng",
        margin="4em",
        # Uncomment if needed for network access
        # host="0.0.0.0",
    )
