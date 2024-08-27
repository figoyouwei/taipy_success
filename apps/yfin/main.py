'''
@author: Youwei Zheng
@target: Main app
@update: 2024.08.13
'''

from datetime import datetime

from taipy.gui import Gui

import pages.calculator as page_calculator
import pages.chatbot as page_chatbot
import pages.yfin as page_yfin

from turing import compute_points
from models.calculator import Level, Point

from tools import download_yfin, process_yfin

if __name__ == "__main__":

    # Create yfinance page
    current_date = datetime.now().strftime('%Y-%m-%d')
    args_in = (
        '^SPX',
        '1d',
        '2024-08-01',
        current_date,
        )
    df = download_yfin(args_in)
    df_pcs = process_yfin(df)
    page_yfin = page_yfin.create_page(df_pcs)
   
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
        "chatbot": page_chatbot
        }

    # Run page
    Gui(pages=pages).run(
        title="Taipy Success",
        debug=True,
        use_reloader=True,
        watermark="Made by CR7",
        margin="4em",
        host="0.0.0.0",
        port=9000
        # base_url="/shggzyapp/" # key to nginx
    )
