import pandas as pd

def clean_crypto_data(raw_data):
  '''
  Cleans raw cryptocurrency data by selecting specific columns and formatting the 'last_updated' column.

  Args:
    raw_data (list of dict): The raw cryptocurrency data.

  Returns:
    pandas.DataFrame: A cleaned DataFrame containing selected columns and formatted 'last_updated' column.
  '''
  df = pd.DataFrame(raw_data)
  cleaned_df = df[['id', 'symbol', 'current_price', 'market_cap', 'last_updated']].copy()
  cleaned_df['last_updated'] = pd.to_datetime(cleaned_df['last_updated'], utc=True)
  cleaned_df['snapshot_date'] = cleaned_df['last_updated'].dt.strftime('%Y-%m-%d')
  return cleaned_df