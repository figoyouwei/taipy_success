"""
@author: Youwei Zheng
@target: yfin app
@update: 2024.09.24
"""

from taipy.gui import Gui
import taipy.gui.builder as tgb

from pages import page_calculator
from pages import page_chatbot
from pages import page_yfin
from pages import page_home

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    
    pages = {
        "/": page_home,
        "yfinance": page_yfin,
        "calculator": page_calculator,
        "chatbot": page_chatbot,
    }

    gui = Gui(pages=pages, css_file="./main.css")

    # Run page
    Gui(pages=pages).run(
        title="Data Dashboard with yfinance",
        debug=True,
        use_reloader=True,
        watermark="Made by CR7",
        margin="4em",
        host="0.0.0.0",
        # port=9000,
        # base_url="/shggzyapp/" # key to nginx
    )
