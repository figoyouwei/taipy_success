"""
@author: Youwei Zheng
@target: Main app
@update: 2024.08.27
"""

from taipy.gui import Gui

import pages.calculator as page_calculator
import pages.chatbot as page_chatbot
from pages.yfin import page_yfin

from turing import compute_points
from models.calculator import Level, Point

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":

    # Create calcuator page
    page_calculator = page_calculator.create_page()

    # Create data instances of calculator model
    levels = Level()
    points = Point()
    points = compute_points(levels)

    # Create calcuator page
    page_chatbot = page_chatbot.create_page()

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
        port=9000,
        # base_url="/shggzyapp/" # key to nginx
    )
