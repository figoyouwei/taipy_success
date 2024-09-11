"""
@author: Youwei Zheng
@target: Main app
@update: 2024.09.03
"""

from taipy.gui import Gui
import taipy.gui.builder as tgb

from apps.yfin.pages import page_calculator
from apps.yfin.pages import page_chatbot
from apps.yfin.pages import page_yfin
from apps.yfin.pages import page_home

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
        title="Taipy Success",
        debug=True,
        use_reloader=True,
        watermark="Made by CR7",
        margin="4em",
        host="0.0.0.0",
        # port=9000,
        # base_url="/shggzyapp/" # key to nginx
    )
