from taipy.gui import Gui
import taipy.gui.builder as tgb

root_page = ""

from pages.about import layout_columns
from pages.sidebar import sidebar_partial
from pages import (
    page_about,
)

with tgb.Page() as page_2:
    with tgb.layout(columns=layout_columns):
        with tgb.part("sidebar"):
            sidebar_partial()
        with tgb.part():
            tgb.navbar()
            tgb.html("h1", "Resume")
            tgb.html("p", "Content to be added")

with tgb.Page() as page_3:
    with tgb.layout(columns=layout_columns):
        with tgb.part("sidebar"):
            sidebar_partial()
        with tgb.part():
            tgb.navbar()
            tgb.html("h1", "Portfolio")
            tgb.html("p", "Content to be added")

pages = {
    "/": root_page,
    "about": page_about,
    "resume": page_2,
    "portfolio": page_3,
}

if __name__ == "__main__":
    gui = Gui(pages=pages, css_file="./static/css/main.css")
    gui.run(
        debug=False,
        title="Personal Website",
        use_reloader=True,
        margin="4em",
        host="0.0.0.0",
        port=5000
        )
    