import os
import sqlite3

import pandas as pd

from logger import logger


def database_path(db_file=None):
  '''
  Resolve the SQLite path. Tests and the CLI can pass a path.
  Otherwise DATABASE_PATH is used, then output/etl_pipeline.db.
  '''
  path = db_file or os.getenv('DATABASE_PATH') or 'output/etl_pipeline.db'
  if not path:
    raise ValueError('The database file path cannot be empty.')
  return path


def create_connection(db_file=None):
  '''
  Open the SQLite database, creating the parent directory when needed.
  '''
  path = database_path(db_file)
  parent = os.path.dirname(path)
  if parent:
    os.makedirs(parent, exist_ok=True)
  return sqlite3.connect(path)


def create_table(db_file=None):
  '''
  Ensure crypto_prices stores one row per coin per snapshot day.

  An older table used the coin id alone as the primary key. That table is
  renamed so the new key can be created. The renamed table is left in place.
  '''
  conn = create_connection(db_file)
  cursor = conn.cursor()
  cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='crypto_prices'"
  )
  if cursor.fetchone():
    columns = [row[1] for row in cursor.execute('PRAGMA table_info(crypto_prices)')]
    if 'snapshot_date' not in columns:
      cursor.execute('ALTER TABLE crypto_prices RENAME TO crypto_prices_legacy')
      logger.info('Renamed the old crypto_prices table. New loads keep one row per coin per day.')

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS crypto_prices (
      id TEXT NOT NULL,
      symbol TEXT,
      current_price REAL,
      market_cap REAL,
      last_updated TEXT,
      snapshot_date TEXT NOT NULL,
      PRIMARY KEY (id, snapshot_date)
    )
  ''')
  conn.commit()
  conn.close()


def insert_data(df, db_file=None):
  '''
  Insert or update one row per coin per snapshot day.

  A second load of the same coin on the same day updates the price.
  It does not add another row.
  '''
  create_table(db_file)
  conn = create_connection(db_file)
  cursor = conn.cursor()

  for _, row in df.iterrows():
    try:
      current_price = 0.0 if pd.isnull(row['current_price']) else float(row['current_price'])
      market_cap = 0.0 if pd.isnull(row['market_cap']) else float(row['market_cap'])
      last_updated = pd.to_datetime(row['last_updated'], utc=True).strftime('%Y-%m-%d %H:%M:%S')
      snapshot_date = row['snapshot_date'] if 'snapshot_date' in row and pd.notnull(row['snapshot_date']) else last_updated[:10]

      cursor.execute('''
        INSERT INTO crypto_prices (id, symbol, current_price, market_cap, last_updated, snapshot_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id, snapshot_date) DO UPDATE SET
          symbol = excluded.symbol,
          current_price = excluded.current_price,
          market_cap = excluded.market_cap,
          last_updated = excluded.last_updated
      ''', (row['id'], row['symbol'], current_price, market_cap, last_updated, snapshot_date))
    except Exception as e:
      logger.error(f"Error processing row {row.get('id', '?')}: {e}")
      continue

  conn.commit()
  conn.close()
