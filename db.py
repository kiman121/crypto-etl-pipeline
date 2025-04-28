import sqlite3
import os
import pandas as pd
import logging

def create_connection(db_file=os.getenv('DATABASE_PATH')):
  '''
  Creates a connection to the SQLite database specified by db_file.

  Args:
    db_file (str): The path to the SQLite database file.

  Returns:
    sqlite3.Connection: A connection object to the SQLite database.
  '''
  # Ensure the database file path is valid and not empty
  if not db_file:
    raise ValueError("The database file path cannot be empty.")
  
  # Create and return the connection object
  conn = sqlite3.connect(db_file)
  return conn

def create_table():
  '''
  Creates the 'crypto_prices' table in the SQLite database if it does not already exist.
  The table contains the following columns:
    - id: Primary key, unique identifier for the cryptocurrency.
    - symbol: The symbol of the cryptocurrency (e.g., BTC, ETH).
    - current_price: The current price of the cryptocurrency.
    - market_cap: The market capitalization of the cryptocurrency.
    - last_updated: The timestamp of the last update.
  '''
  # Connect to the SQLite database using the path from the environment variable
  conn = create_connection()
  cursor = conn.cursor()

  # Create the table if it does not already exist
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS crypto_prices (
      id TEXT PRIMARY KEY,
      symbol TEXT,
      current_price REAL,
      market_cap REAL,
      last_updated TEXT
    )
  ''')

  # Commit the changes and close the connection
  conn.commit()
  conn.close()

def insert_data(df):
  '''
  Inserts or updates data in the 'crypto_prices' table from a pandas DataFrame.
  Each row in the DataFrame is inserted or replaced based on the primary key (id).

  Args:
    df (pandas.DataFrame): A DataFrame containing the following columns:
    - id: Unique identifier for the cryptocurrency.
    - symbol: The symbol of the cryptocurrency (e.g., BTC, ETH).
    - current_price: The current price of the cryptocurrency.
    - market_cap: The market capitalization of the cryptocurrency.
    - last_updated: The timestamp of the last update.
  '''
  conn = create_connection()  # Create a new connection
  cursor = conn.cursor()

  # Iterate over each row in the DataFrame and insert or replace the data
  for _, row in df.iterrows():
    try:
      # Validate and convert current_price and market_cap to float (handle None or NaN)
      current_price = row['current_price']
      market_cap = row['market_cap']

      # Handle NaN or None values
      if pd.isnull(current_price):
        current_price = 0.0  # Set to 0 if NaN or None
      if pd.isnull(market_cap):
        market_cap = 0  # Set to 0 if NaN or None

      # Ensure current_price is a float
      if not isinstance(current_price, (int, float)):
        current_price = float(current_price)

      # Ensure market_cap is a float or int
      if not isinstance(market_cap, (int, float)):
        market_cap = float(market_cap)

      # Ensure timestamp format for SQLite
      last_updated = pd.to_datetime(row['last_updated']).strftime('%Y-%m-%d %H:%M:%S')

      # Insert or replace the row in the database
      cursor.execute('''
          INSERT OR REPLACE INTO crypto_prices (id, symbol, current_price, market_cap, last_updated)
          VALUES (?, ?, ?, ?, ?)
      ''', (row['id'], row['symbol'], current_price, market_cap, last_updated))
    except Exception as e:
      logging.error(f"Error processing row {row['id']}: {e}")
      continue  # Skip the row and continue with the next

  # Commit the changes and close the connection
  conn.commit()
  conn.close()

def initialize_db():
  '''
  Initializes the database by ensuring the necessary tables exist.
  Calls create_table to set up the schema.
  '''
  create_table()

initialize_db()