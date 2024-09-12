from taipy.gui import Gui
import taipy.gui.builder as tgb

with tgb.Page() as page:
    with tgb.layout(columns="2 8"):
        with tgb.part("sidebar"):
            tgb.html("h2", "Richard Hendricks")
            tgb.html("p", "Founder of Pied Piper")
        with tgb.part():
            tgb.navbar()

root_page = page
page_1 = "Page About"
page_2 = "Page Resume"
page_3 = "Page Portfolio"

pages = {
    "/": root_page, 
    "about": "Page About", 
    "resume": "Page Resume", 
    "portfolio": "Page Portfolio"
}

if __name__ == "__main__":
    Gui(pages=pages).run()