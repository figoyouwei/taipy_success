import polars as pl
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters

DATABASE_HOST = "43.134.197.145"
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

def load_data_from_postgres(query):
    """
    Load data from PostgreSQL database and return as a Polars DataFrame.
    """
    try:
        # Establish a connection to the database
        conn = psycopg2.connect(
            host=DATABASE_HOST,  # This should be an IP address or hostname
            port=DATABASE_PORT,
            user=DATABASE_USER,
            dbname=DATABASE_NAME,
            password=DATABASE_PASSWORD,
        )
        
        # Create a cursor object
        cur = conn.cursor()
        
        # Execute the query
        cur.execute(query)
        
        # Fetch all rows
        rows = cur.fetchall()
        
        # Get column names
        column_names = [desc[0] for desc in cur.description]
        
        # Close cursor and connection
        cur.close()
        conn.close()
        
        # Create a Polars DataFrame
        df = pl.DataFrame(rows, schema=column_names, orient="row")
        
        return df
    
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None


if __name__ == "__main__":
    # Example usage:
    query = "SELECT * FROM datei_ppi"
    df = load_data_from_postgres(query)
    
    if df is not None:
        print(df.head())
    else:
        print("Failed to load data from the database.")
