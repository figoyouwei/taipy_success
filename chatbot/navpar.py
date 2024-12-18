from taipy.gui import Gui, State, notify, navigate
import taipy.gui.builder as tgb

results_ready = False
nav_parameters = {}

def on_navigate(state: State, page_name: str, parameters: dict) -> str:
    print("on_navigate called...")
    print(page_name, parameters)
    state.nav_parameters = parameters
    return page_name

with tgb.Page() as root_page:
    tgb.text("# Results Page", mode="md")
    tgb.text("Navigation Parameters:", mode="md")
    tgb.text("*{nav_parameters}*", mode="md")

pages = {
    "/": root_page,
}

# http://localhost:5000/results?id=Florian&age=32
Gui(pages=pages).run()
