'''
@author: Youwei Zheng
@target: Getting started with great_tables v0.10.0
@update: 2024.07.29
'''

from great_tables import GT
from great_tables.data import sp500

# ------------------------------
# Historical sp500 data with title, header and formatted columns.
# ------------------------------

# Define the start and end dates for the data range
start_date = "2010-06-07"
end_date = "2010-06-14"

# Filter sp500 using Pandas to dates between `start_date` and `end_date`
sp500_mini = (
    sp500[
        (sp500["date"] >= start_date) & 
        (sp500["date"] <= end_date)
    ]
)

sp500_mini
type(sp500_mini)


sp500_mini

# 创建并自定义表格
(
    GT(sp500_mini)
    .tab_header(title="标普500指数", subtitle=f"{start_date} 至 {end_date}")
    #.fmt_currency(columns=["open", "high", "low", "close"])  # 格式化货币列
    .fmt_date(columns="date", date_style="wd_m_day_year")   # 格式化日期列
    .fmt_number(columns="volume", compact=True)             # 格式化数字列
    .cols_hide(columns="adj_close")                  # 隐藏调整后收盘价列
)

# ------------------------------
# Getting started with yfinance's latest sp500 data.
# ------------------------------

import yfinance as yf
import polars as pl

# Define the ticker symbol for S&P 500
ticker_symbol = "^GSPC"

start_date = "2024-07-22"
end_date = "2024-07-27"

# Fetch historical data for the S&P 500
sp500_data = yf.download(
    ticker_symbol, 
    start=start_date, 
    end=end_date
)

# Reset the index to make 'Date' a column
sp500_data.reset_index(inplace=True)

# Display the data
print(sp500_data.head())
type(sp500_data.head())

# Process pl.dataframe
sp500_pl = (
    pl.from_pandas(sp500_data)
    .drop("Adj Close")
    .with_columns([
        pl.col("Open").round(2).alias("Open"),
        pl.col("High").round(2).alias("High"),
        pl.col("Low").round(2).alias("Low"),
        pl.col("Close").round(2).alias("Close"),
        (pl.col("Volume") / 1_000_000_000).round(2).alias("Volume"),
    ])
)
sp500_pl

# 创建并自定义表格
(
    GT(sp500_pl)
        .tab_header(
            title="S&P Index", 
            subtitle=f"From {start_date} to {end_date}")
        #.fmt_currency(columns=["open", "high", "low", "close"])
        .fmt_date(columns="Date", date_style="wd_m_day_year")
        #.fmt_number(columns="volume", compact=True)
        #.cols_hide(columns="adj_close")
        .save("sp500.png", scale=3)
)
