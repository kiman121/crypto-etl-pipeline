from db import insert_data
from logger import logger
import os

def csv_path():
  '''
  OUTPUT_CSV is the documented path. CSV_PATH is still accepted.
  '''
  return os.getenv('OUTPUT_CSV') or os.getenv('CSV_PATH') or 'output/data.csv'


def save_to_csv(df):
  '''
  Saves the latest snapshot to a CSV file, replacing the previous file.
  '''
  path = csv_path()
  parent = os.path.dirname(path)
  if parent:
    os.makedirs(parent, exist_ok=True)
  df.to_csv(path, index=False)
  logger.info(f'Data saved to CSV at {path}')

def save_to_db(df):
  '''
  Saves the cleaned DataFrame to the SQLite database.

  This function inserts or updates the data in the database using the 
  `insert_data` function from the `db` module.

  Args:
    df (pandas.DataFrame): The cleaned DataFrame containing cryptocurrency data.
  '''
  # Insert or update data in the database
  insert_data(df)
  # Log the success message indicating data has been saved
  logger.info('Data saved to SQLite database')
