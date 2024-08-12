'''
@author: Youwei Zheng
@target: scenario for Beginner with yfinance data
@update: 2024.08.12
'''

# ------------------------------
# Creating sample dataset
# ------------------------------

import yfinance as yf
import pandas as pd
import polars as pl

# Define the ticker symbol for S&P 500
ticker_symbol = '^GSPC'

# Fetch the data for the year 2024
sp500_data_yf = yf.download(ticker_symbol, start='2024-01-01', end='2024-12-31')
sp500_data_yf.reset_index(inplace=True)

# Display the first few rows of the data
# sp500_data_pl = pl.from_pandas(sp500_data_yf)
# sp500_data_pl
# print(sp500_data_pl.head())

# ------------------------------
# Creating task function
# ------------------------------

def task_format_sp500(sp500_data: pd.DataFrame) -> pl.DataFrame:
    # Process pl.dataframe
    sp500_data_pl = (
        pl.from_pandas(sp500_data)
        .drop("Adj Close")
        # Format existing 5 indicators
        .with_columns([
            pl.col("Open").round(2).alias("Open"),
            pl.col("High").round(2).alias("High"),
            pl.col("Low").round(2).alias("Low"),
            pl.col("Close").round(2).alias("Close"),
            (pl.col("Volume") / 1_000_000_000).round(2).alias("Volume"),
        ])
        # Compute new indicator Range
        .with_columns([
            (pl.col("High") - pl.col("Low")).alias("Range")
        ])    
        # Compute percentage of Range to Open
        .with_columns([
            ((pl.col("Range") / pl.col("Open"))*100).round(2).alias("RangePct")
        ])
        .sort(by="Date", descending=True)
    )
    
    return sp500_data_pl
    
# sp500_data_pl = task_format_sp500(sp500_data)
# sp500_data_pl.head(20)

# ------------------------------
# Creating scenario
# ------------------------------

from taipy import Config as tpc

# Configuration of nodes
node_sp500_data_yf = tpc.configure_data_node("sp500_data_yf")
node_sp500_data = tpc.configure_data_node("sp500_data")

# Configuration of tasks
task_sp500 = tpc.configure_task(
    id="task_sp500_data",
    function=task_format_sp500,
    input=node_sp500_data_yf,
    output=node_sp500_data
    )

# Configuration of scenario
scenario_sp500 = tpc.configure_scenario(
    id="sp500",
    task_configs=[task_sp500]
    )

import taipy as tp

if __name__ == "__main__":
    # Run of the Core
    tp.Core().run()

    # Creation of the scenario and execution
    scenario = tp.create_scenario(scenario_sp500)
    scenario.sp500_data_yf.write(sp500_data_yf)
    tp.submit(scenario)

    sp500_data_pl = scenario.sp500_data.read()
    sp500_data_pl