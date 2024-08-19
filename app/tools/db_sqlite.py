'''
@author: Youwei Zheng
@target: database tools with sqlite using sqlalchemy
@update: 2024.08.19
'''

# ------------------------------
# Database Manager
# ------------------------------

import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
import pandas as pd

class DB_SQLITE_MANAGER:
    def __init__(self, db_path):
        self.db_path = db_path
        self._check_database_existence()
        self.engine = create_engine(f'sqlite:///{self.db_path}')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.metadata = MetaData()

    def _check_database_existence(self):
        if not os.path.exists(self.db_path):
            print(f"Database at '{self.db_path}' does not exist. A new database will be created.")
        else:
            print(f"Database at '{self.db_path}' found. Connecting to the existing database.")

    def create_table(self, table_name: str, model):
        # Reflect existing tables using MetaData
        self.metadata.reflect(bind=self.engine)

        # Check if the table already exists
        if table_name in self.metadata.tables:
            print(f"Table {table_name} already exists.")
            return self.metadata.tables[table_name]

        # Dynamically create a table based on the given model and table name
        dynamic_table = Table(
            table_name,
            model.metadata,
            *(column.copy() for column in model.__table__.columns),
            extend_existing=True
        )

        # Create the table in the database
        model.metadata.create_all(self.engine)
        print(f"Table {table_name} has been created.")

        # Reflect the table again to ensure it's added to the metadata
        self.metadata.reflect(bind=self.engine)
        return self.metadata.tables[table_name]
    
    def commit_data(self, table, data: pd.DataFrame):
        # Convert DataFrame to a list of dictionaries
        records = data.to_dict(orient='records')

        # Prepare the insert statement
        insert_stmt = table.insert().values(records)

        # Execute the insert statement
        self.session.execute(insert_stmt)
        self.session.commit()
        print(f"Records have been inserted.")

    def query_data(self, table):
        # Query the data
        result = self.session.execute(table.select()).fetchall()
        print(f"All data from the table '{table.name}' has been fetched.")
        return result

    def empty_data(self, table):
        # Delete all rows from the table
        delete_stmt = table.delete()
        self.session.execute(delete_stmt)
        self.session.commit()
        print(f"All data from the table '{table.name}' has been deleted.")