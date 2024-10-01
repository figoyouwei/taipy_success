import taipy.gui.builder as tgb

from pages.sidebar import sidebar_partial

layout_columns = "2 8"

with tgb.Page() as page:
    with tgb.layout(columns=layout_columns):
        with tgb.part("sidebar"):
            sidebar_partial()

        with tgb.part():
            tgb.navbar()
            tgb.html("h2", "About Me")

