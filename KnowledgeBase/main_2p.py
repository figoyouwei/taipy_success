from taipy.gui import Gui
from pages.home import home_md
from pages.temperature import temperature_md

pages = {
    "home": home_md, 
    "temperature": temperature_md
    }

Gui(pages=pages).run()