'''
@author: Youwei Zheng
@target: Main app
@update: 2024.07.25
'''

from taipy.gui import Gui
from gui import setup_gui, filter_refresh, filter_reset
from turing import compute_points
from models import Level, Point

if __name__ == "__main__":

    # Create instances of data model
    levels = Level()
    points = Point()
    points = compute_points(levels)
            
    # Create instance of page
    page = setup_gui(filter_refresh, filter_reset)

    # Run page
    Gui(page).run(
        title="Taipy Success",
        debug=True,
        use_reloader=True,
        watermark="Made by CR7",
        margin="4em",
        host="0.0.0.0",
        port=9000
        # base_url="/shggzyapp/" # key to nginx
    )
