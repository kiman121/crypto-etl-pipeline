import sqlite3
import os

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
  conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
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
  # Connect to the SQLite database using the path from the environment variable
  conn = sqlite3.connect(os.getenv('DATABASE_PATH'))
  cursor = conn.cursor()

  # Iterate over each row in the DataFrame and insert or replace the data
  for _, row in df.iterrows():
    cursor.execute('''
      INSERT OR REPLACE INTO crypto_prices (id, symbol, current_price, market_cap, last_updated)
      VALUES (?, ?, ?, ?, ?)
    ''', (row['id'], row['symbol'], row['current_price'], row['market_cap'], row['last_updated']))

  # Commit the changes and close the connection
  conn.commit()
  conn.close()

