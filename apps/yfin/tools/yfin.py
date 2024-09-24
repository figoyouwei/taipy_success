'''
@author: Youwei Zheng
@target: tools with yfinance
@update: 2024.09.24
'''

import pandas as pd
import polars as pl

# ------------------------------
# Download dataset
# ------------------------------

import yfinance as yf
import pandas as pd
from datetime import datetime

def download_yfin(args_in: tuple) -> pd.DataFrame:
    """
    Downloads historical stock data from Yahoo Finance.

    Parameters:
    - args_in (tuple): A tuple containing the ticker symbol, interval, start date, and end date.
    ^SPX, ^NDX
    ES=F, NQ=F
    
    Returns:
    - pd.DataFrame: DataFrame containing the historical stock data.
    """

    ticker_symbol, interval, start_date, end_date = args_in

    # Validate input parameters
    try:
        if end_date != None:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        else:
            datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.")

    valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    if interval not in valid_intervals:
        raise ValueError(f"Invalid interval '{interval}'. Valid intervals are: {valid_intervals}")

    if not ticker_symbol:
        raise ValueError("Ticker symbol must not be empty.")

    # Download data
    try:
        print("Downloading from yfin...")
        if end_date != None:
            data_yf = yf.download(tickers=ticker_symbol, interval=interval, start=start_date, end=end_date)
        else:
            data_yf = yf.download(tickers=ticker_symbol, interval=interval, start=start_date)
        data_yf.reset_index(inplace=True)
    except Exception as e:
        raise RuntimeError(f"An error occurred while downloading data: {e}")

    # Check if the index is called 'Date' and rename it to 'Datetime'
        if data_yf.index.name == 'Date':
            data_yf.index.name = 'Datetime'    

    return data_yf

# ------------------------------
# Process dataset
# ------------------------------

def process_yfin(data_yfin: pd.DataFrame) -> pd.DataFrame:
    print("Processing data from yfin...")
    # Note: List of columns in the desired order
    column_order = [
        "Datetime", "candle_type", 
        "High-Low", "Open-Close",
        "Open", "Close", "High", "Low", "Volume", 
        ]

    # Process pl.dataframe
    data_yfin_pl = (
        pl.from_pandas(data=data_yfin)
        .drop("Adj Close")
        # Format existing 5 indicators
        .with_columns([
            pl.col("Open").round(2).alias("Open"),
            pl.col("High").round(2).alias("High"),
            pl.col("Low").round(2).alias("Low"),
            pl.col("Close").round(2).alias("Close"),
            (pl.col("Volume") / 1_000_000_000).round(2).alias("Volume"),
        ])
        # Note: BOT or SOLD
        .with_columns(
            pl.when(pl.col("Close") > pl.col("Open"))
            .then(pl.lit("BOT"))
            .otherwise(pl.lit("SOLD"))
            .alias("candle_type")
        )
        # Note: High-Low
        .with_columns([
            (pl.col("High") - pl.col("Low")).round(2).alias("High-Low")
        ])    
        # Note: Open-Close
        .with_columns([
            (abs(pl.col("Open") - pl.col("Close"))).round(2).alias("Open-Close")
        ])        
        # Compute percentage of Range to Open
        # .with_columns([
        #     ((pl.col("Range") / pl.col("Open"))*100).round(2).alias("RangePct")
        # ])
        .sort(by="Datetime", descending=False)
        .select(column_order)
    )
    
    data_yfin_pd = data_yfin_pl.to_pandas()
    data_yfin_pd.set_index('Datetime', inplace=True)
    
    return (data_yfin_pl, data_yfin_pd)

# ------------------------------
# Creating scenario
# Note: not useful
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
    symbol, itv, start_date, end_date = (
        '^SPX',
        '30m',
        '2024-08-01',
        '2024-08-13',
    )

    data_input = download_yfin(
        ticker_symbol=symbol,
        interval=itv,
        start_date=start_date,
        end_date=end_date
        )
    data_input

    # Creation of the scenario and execution
    scenario = create_scenario(
        tool2call=process_yfin,
        node_input_name="data_in",
        node_output_name="data_out",
        task_id="task",
        scenario_id="scenario"
    )
    
    scenario.data_in.write(data_input)
    tp.submit(scenario)

    data_sp500 = scenario.data_out.read()
    type(data_sp500)