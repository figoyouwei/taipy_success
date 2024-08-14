'''
@author: Youwei Zheng
@target: taipy scenario with yfinance
@update: 2024.08.14
'''

import pandas as pd
import polars as pl

# ------------------------------
# Download dataset
# ------------------------------

def download_data_sp500():
    import yfinance as yf

    # Define the ticker symbol for S&P 500
    ticker_symbol = '^GSPC'

    # Fetch the data for the year 2024
    sp500_data_yf = yf.download(ticker_symbol, start='2024-01-01', end='2024-12-31')
    sp500_data_yf.reset_index(inplace=True)

    return sp500_data_yf

# ------------------------------
# Process dataset
# ------------------------------

def process_data_sp500(sp500_data: pd.DataFrame) -> pd.DataFrame:
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
            (pl.col("High") - pl.col("Low")).round(2).alias("Range")
        ])    
        # Compute percentage of Range to Open
        .with_columns([
            ((pl.col("Range") / pl.col("Open"))*100).round(2).alias("RangePct")
        ])
        .sort(by="Date", descending=True)
    )
    
    return sp500_data_pl.to_pandas()

# ------------------------------
# Creating scenario
# ------------------------------

import taipy as tp
from taipy import Config as tpc

from typing import Callable

def create_scenario(
    tool2call: Callable, 
    node_input_name: str,
    node_output_name: str,
    task_id: str, 
    scenario_id: str
    ):

    # Configurate nodes
    node_input = tpc.configure_data_node(node_input_name)
    node_output = tpc.configure_data_node(node_output_name)

    # Configurate task
    task_cfg = tpc.configure_task(
        id=task_id,
        function=tool2call,
        input=node_input,
        output=node_output
        )

    # Configuration of scenario
    scenario_cfg = tpc.configure_scenario(
        id=scenario_id,
        task_configs=[task_cfg]
        )

    # Run core
    tp.Core().run()

    # Create scenario client
    scenario = tp.create_scenario(scenario_cfg)

    return scenario

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    # Run data
    data_input = download_data_sp500()
    data_input

    # Creation of the scenario and execution
    scenario = create_scenario(
        tool2call=process_data_sp500,
        node_input_name="data_in",
        node_output_name="data_out",
        task_id="task",
        scenario_id="scenario"
    )
    
    scenario.data_in.write(data_input)
    tp.submit(scenario)

    data_sp500 = scenario.data_out.read()
    type(data_sp500)