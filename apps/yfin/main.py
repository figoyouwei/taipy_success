"""
@author: Youwei Zheng
@target: Main app
@update: 2024.09.03
"""

from taipy.gui import Gui

from apps.yfin.pages.calculator import page as page_calculator
from apps.yfin.pages.chatbot import page as page_chatbot
from apps.yfin.pages.yfin import page as page_yfin

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":

    pages = {
        "/": "<center><|navbar|></center>",
        "yfinance": page_yfin,
        "calculator": page_calculator,
        "chatbot": page_chatbot,
    }

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
