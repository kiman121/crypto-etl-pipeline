import pandas as pd
from db import insert_data
from logger import logger
import os

def save_to_csv(df):
  '''
  Saves the given DataFrame to a CSV file.

  The file path is retrieved from the environment variable 'CSV_PATH'.

  Args:
    df (pandas.DataFrame): The DataFrame to be saved as a CSV file.
  '''
  # Save the DataFrame to a CSV file without including the index
  df.to_csv(os.getenv('CSV_PATH'), index=False)
  # Log the success message with the file path
  logger.info(f'Data saved to CSV at {os.getenv("CSV_PATH")}')

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
