import json
import sqlite3
from pathlib import Path

from db import insert_data
from schedule import run_on_interval
from transform import clean_crypto_data

FIXTURE = Path(__file__).parent / 'fixtures' / 'markets.json'


def load_fixture():
  return json.loads(FIXTURE.read_text())


def test_clean_keeps_the_record_fields_and_the_snapshot_day():
  cleaned = clean_crypto_data(load_fixture())
  assert list(cleaned['id']) == ['bitcoin', 'ethereum']
  assert list(cleaned['snapshot_date']) == ['2026-10-28', '2026-10-28']
  assert 'name' not in cleaned.columns


def test_loading_the_same_day_twice_keeps_one_row_per_coin(tmp_path):
  db_file = tmp_path / 'prices.db'
  cleaned = clean_crypto_data(load_fixture())

  insert_data(cleaned, db_file=db_file)
  cleaned.loc[cleaned['id'] == 'bitcoin', 'current_price'] = 65000
  insert_data(cleaned, db_file=db_file)

  conn = sqlite3.connect(db_file)
  rows = conn.execute(
    'SELECT id, current_price, snapshot_date FROM crypto_prices ORDER BY id'
  ).fetchall()
  conn.close()

  assert rows == [
    ('bitcoin', 65000.0, '2026-10-28'),
    ('ethereum', 0.0, '2026-10-28'),
  ]


def test_a_later_day_is_a_new_row(tmp_path):
  db_file = tmp_path / 'prices.db'
  cleaned = clean_crypto_data(load_fixture())
  insert_data(cleaned, db_file=db_file)

  next_day = cleaned.copy()
  next_day['snapshot_date'] = '2026-10-29'
  insert_data(next_day.loc[next_day['id'] == 'bitcoin'], db_file=db_file)

  conn = sqlite3.connect(db_file)
  count = conn.execute('SELECT COUNT(*) FROM crypto_prices').fetchone()[0]
  conn.close()
  assert count == 3


def test_scheduler_runs_and_stops_cleanly():
  calls = []

  def runner():
    calls.append('run')

  def stop_after_one_wait(_seconds):
    raise KeyboardInterrupt

  run_on_interval(15, runner, sleep=stop_after_one_wait)
  assert calls == ['run']
