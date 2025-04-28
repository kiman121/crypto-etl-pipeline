# Python ETL Pipeline - Crypto Data

This project demonstrates an ETL pipeline for extracting cryptocurrency data from the CoinGecko API, transforming it, and saving it to both CSV and SQLite.

## Features

- **Extract**: Fetch real-time cryptocurrency data (e.g., Bitcoin, Ethereum) from the CoinGecko API.
- **Transform**: Clean and structure the data, including handling missing values and converting types.
- **Load**: Store the data in both a SQLite database and a CSV file.
- **Error Handling**: Implement logging for tracking activity and errors.
- **Command-Line Arguments**: Support for specifying the currency (USD or other) through command-line arguments.

## Technologies Used

- **Python**
- **pandas**: For data processing and transformation.
- **sqlite3**: For storing processed data in an SQLite database.
- **requests**: For fetching data from the CoinGecko API.
- **logging**: For activity tracking and error handling.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file with the following content:

   ```
   API_URL=https://api.coingecko.com/api/v3/coins/markets
   DATABASE_PATH=output/etl_pipeline.db
   OUTPUT_CSV=output/data.csv
   ```

3. Run the ETL pipeline:

   ```
   python main.py
   ```

   Alternatively, you can specify the currency (USD or other) using a command-line argument:

   ```
   python main.py --currency usd
   ```
