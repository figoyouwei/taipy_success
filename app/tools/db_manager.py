'''
@author: Youwei Zheng
@target: database tools with sqlite using sqlalchemy
@update: 2024.08.19
'''

# ------------------------------
# Database Manager
# ------------------------------

from functools import wraps
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

    def create_table(self, model, table_name=None):
        # Use the model's __tablename__ as the default table name if not provided
        self.table_name = table_name or model.__tablename__

        # Reflect existing tables using MetaData
        self.metadata.reflect(bind=self.engine)

        # Check if the table already exists
        if self.table_name in self.metadata.tables:
            print(f"Table {self.table_name} already exists.")
            self.table = self.metadata.tables[self.table_name]
        else:
            # Dynamically create a table based on the given model and table name
            self.table = Table(
                self.table_name,
                model.metadata,
                *(column.copy() for column in model.__table__.columns),
                extend_existing=True
            )

            # Create the table in the database
            model.metadata.create_all(self.engine)
            print(f"Table {self.table_name} has been created.")

            # Reflect the table again to ensure it's added to the metadata
            self.metadata.reflect(bind=self.engine)
            self.table = self.metadata.tables[self.table_name]

    def commit_data(self, data: pd.DataFrame):
        if self.table is None:
            raise ValueError("Table is not set. Ensure 'create_table' is called before committing data.")
        
        # Convert DataFrame to a list of dictionaries
        records = data.to_dict(orient='records')

        # Prepare the insert statement
        insert_stmt = self.table.insert().values(records)

        # Execute the insert statement
        self.session.execute(insert_stmt)
        self.session.commit()
        print(f"Records have been inserted into {self.table_name}.")

    def commit(self, model):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print("Decorator called!")
                # Call the decorated function (e.g., download_yfin)
                df = func(*args, **kwargs)
                
                # Create the table (if not exists) and get the table object
                table = self.create_table(model)
                
                # Commit the data to the table
                self.commit_data(table, df)
                
                return df  # Optionally return the DataFrame if needed
            return wrapper
        return decorator

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