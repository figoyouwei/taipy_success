'''
@author: Youwei Zheng
@target: Taipy Navbar
@update: 2024.09.09
'''

from taipy import Gui
import taipy.gui.builder as tgb

# ------------------------------
# Create page
# ------------------------------

navbar_lov = [
    ("Calculator", "Calculator Page"),
    ("Chatbot", "Chatbot Page"),
    ("https://taipy.io/", "Taipy Home")
]

with tgb.Page() as page:
    tgb.navbar(
        lov="{navbar_lov}"
        )

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    Gui(page=page).run(
        use_reloader=True,
        debug=True,
    )