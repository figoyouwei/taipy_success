"""
@author: Youwei Zheng
@target: Candle plot with mpf
@update: 2024.09.24
"""

args_yf = (
    '^NDX',
    '15m',
    '2024-09-19',
    '2024-09-24',
)

import mplfinance as mpf
from tools import download_yfin, process_yfin

# ! yf package must be updated and has Datetime bug.
df_yf = download_yfin(args_in=args_yf)
(df_pl, df_pd) = process_yfin(data_yfin=df_yf)
df_pd

# ------------------------------
# Main app
# ------------------------------

from taipy.gui import Gui

if __name__ == "__main__":
    print("Visualizing candles...")

    fig = mpf.plot(
        data=df_pd, 
        type="candle", 
        style="charles",
        )
    
    Gui("<|chart|figure={fig}|height=800px|>").run(port=5000)