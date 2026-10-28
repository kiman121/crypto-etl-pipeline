import argparse
from extract import fetch_crypto_data
from transform import clean_crypto_data
from load import save_to_csv, save_to_db
from logger import logger

def run_etl(currency='usd'):
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
    raw_data = fetch_crypto_data(currency)
    
    # Step 2: Transform data
    cleaned_data = clean_crypto_data(raw_data)
    
    # Step 3: Load data to CSV
    save_to_csv(cleaned_data)
    
    # Step 4: Load data to SQLite database
    save_to_db(cleaned_data)
    
    # Log success message
    logger.info('ETL process completed successfully')
  except Exception as e:
    logger.error(f'ETL process failed: {e}')
    raise

def parse_args():
  '''
  Parses command-line arguments for the ETL process.

  This function sets up an argument parser to allow the user to specify
  the currency for which cryptocurrency data should be fetched. If no
  currency is provided, it defaults to 'usd'.

  Returns:
    argparse.Namespace: Parsed command-line arguments containing the currency.
  '''
  # Create an argument parser with a description of the ETL process
  parser = argparse.ArgumentParser(description='ETL process for cryptocurrency data.')
  
  # Add an optional argument for specifying the currency
  parser.add_argument(
      '--currency', 
      type=str, 
      default='usd', 
      help='Currency to fetch data in (default: usd)'
  )
  parser.add_argument(
      '--every-minutes',
      type=int,
      default=0,
      help='Run on a loop. 0 runs once and exits (default: 0)'
  )
  
  # Parse and return the command-line arguments
  return parser.parse_args()

if __name__ == '__main__':
  args = parse_args()
  if args.every_minutes and args.every_minutes > 0:
    from schedule import run_on_interval
    run_on_interval(args.every_minutes, lambda: run_etl(currency=args.currency))
  else:
    run_etl(currency=args.currency)