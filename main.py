from extract import fetch_crypto_data
from transform import clean_crypto_data
from load import save_to_csv, save_to_db
from logger import logger

def run_etl():
  '''
  Executes the ETL (Extract, Transform, Load) process for cryptocurrency data.

  Steps:
  1. Extract data from an API.
  2. Transform the raw data into a cleaned format.
  3. Load the cleaned data into a CSV file.
  4. Load the cleaned data into an SQLite database.
  '''
  try:
    # Step 1: Extract data from API
    raw_data = fetch_crypto_data()
    
    # Step 2: Transform data
    cleaned_data = clean_crypto_data(raw_data)
    
    # Step 3: Load data to CSV
    save_to_csv(cleaned_data)
    
    # Step 4: Load data to SQLite database
    save_to_db(cleaned_data)
    
    # Log success message
    logger.info('ETL process completed successfully')
  except Exception as e:
    # Log error message if ETL process fails
    logger.error(f'ETL process failed: {e}')

if __name__ == '__main__':
  # Run the ETL process
  run_etl()