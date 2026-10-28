# Crypto ETL pipeline

Python ETL for a public market API. One run fetches the top coins, keeps the fields the record needs, and stores them. Run it again the same day and the price is updated in place. The next day is a new row.

This is the public sample of the pipeline shape I use at work: fetch, parse into a record, load, and run on a schedule. The source here is CoinGecko. The client work stays in the client repository.

## What a run proves

- Extract from an HTTP API (`extract.py`)
- Transform to a stable record: id, symbol, price, market cap, timestamp, snapshot day (`transform.py`)
- Load the latest snapshot to CSV, and one row per coin per day to SQLite (`load.py`, `db.py`)
- A second load of the same coin and day does not insert a duplicate
- `--every-minutes` repeats the run
- `tests/test_pipeline.py` runs against a saved API fixture, with no network

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

`.env` is optional. Without it, the pipeline uses the CoinGecko markets URL, `output/etl_pipeline.db`, and `output/data.csv`.

## Run

```bash
python main.py --currency usd
python main.py --every-minutes 60
pytest
```

CoinGecko's public API is rate limited. The tests do not call it.

If you already have a database from the previous version of this repo, the first new load renames that table to `crypto_prices_legacy` and starts the daily table beside it.
