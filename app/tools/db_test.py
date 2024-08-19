'''
@author: Youwei Zheng
@target: test database manager
@update: 2024.08.19
'''

from app.models.yfin import YfinSPX
from app.tools.db_sqlite import DBManager
import pandas as pd

# ------------------------------
# Main app
# ------------------------------

if __name__ == "__main__":
    # Initialize DBManager
    db_manager = DBManager('app/databases/yfin.db')

    # Create the table and get the table object
    table_spx_daily = db_manager.create_table('spx_daily', YfinSPX)
    table_spx_daily
    
    # Example pandas DataFrame
    data = {
        'Date': ['2024-08-17', '2024-08-18', '2024-08-19'],
        'Open': [4400.0, 4450.0, 4500.0],
        'High': [4500.0, 4550.0, 4600.0],
        'Low': [4350.0, 4400.0, 4450.0],
        'Close': [4450.0, 4500.0, 4550.0],
        'Volume': [1500000, 1600000, 1700000]
    }
    df = pd.DataFrame(data)

    # Commit the data to the table
    db_manager.commit_data(table_spx_daily, df)

    # Query and print the data
    result = db_manager.query_data(table_spx_daily)
    for row in result:
        print(row)