import requests
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()

def fetch_crypto_data(currency):
  '''
  Fetch cryptocurrency data from the API.

  This function retrieves the top 10 cryptocurrencies by market cap in USD.
  It uses the API URL specified in the environment variables and sends a GET
  request with the required parameters.

  Returns:
    list: A list of cryptocurrency data in JSON format.

  Raises:
    requests.exceptions.RequestException: If there is an error during the API request.
  '''
  # Get the API URL from environment variables
  url = os.getenv('API_URL')

  # Define the query parameters for the API request
  params = {
    'vs_currency': currency,  # Currency to convert prices to
    'order': 'market_cap_desc',  # Order by market cap in descending order
    'per_page': 10,  # Number of results per page
    'page': 1,  # Page number to fetch
    'sparkline': False  # Exclude sparkline data
  }

  try:
    # Log the start of the API request
    logger.info('Fetching data from API...')
    
    # Make the GET request to the API
    response = requests.get(url, params=params)
    
    # Raise an exception for HTTP errors
    response.raise_for_status()
    
    # Return the JSON response
    return response.json()
  except requests.exceptions.RequestException as e:
    # Log the error and re-raise the exception
    logger.error(f'Error fetching data from API: {e}')
    raise
