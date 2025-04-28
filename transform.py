import pandas as pd

def clean_crypto_data(raw_data):
  '''
  Cleans raw cryptocurrency data by selecting specific columns and formatting the 'last_updated' column.

  Args:
    raw_data (list of dict): The raw cryptocurrency data.

  Returns:
    pandas.DataFrame: A cleaned DataFrame containing selected columns and formatted 'last_updated' column.
  '''
  # Convert the raw data into a pandas DataFrame
  df = pd.DataFrame(raw_data)
  
  # Select specific columns of interest
  cleaned_df = df[['id', 'symbol', 'current_price', 'market_cap', 'last_updated']]
  
  # Convert the 'last_updated' column to datetime format
  cleaned_df.loc[:, 'last_updated'] = pd.to_datetime(cleaned_df['last_updated'])

  
  return cleaned_df