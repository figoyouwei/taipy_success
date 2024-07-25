'''
@author: Youwei Zheng
@target: Main app
@update: 2024.07.25
'''

from taipy.gui import Gui
from gui import setup_gui, on_filter, reset_filters
from turing import levels

if __name__ == "__main__":

    # ------------------------------
    # 加载数据与初始化参数
    # ------------------------------

    starting_level = 565.16
    target_level = 540.00

    # Initial turing.
    (
        points_net, 
        points_pct
    ) = levels(
        starting_level=starting_level,
        target_level=target_level
    )
    
    # use_reloader=True when changes are made
    page = setup_gui(on_filter, reset_filters)

    Gui(page).run(
        title="Taipy Deployment on Heroku",
        debug=True,
        use_reloader=True,
        watermark="Made by CR7",
        margin="4em",
        # host="0.0.0.0",
        # base_url="/shggzyapp/" # key to nginx
    )
