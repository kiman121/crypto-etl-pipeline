import time

from logger import logger


def run_on_interval(every_minutes, runner, sleep=time.sleep):
  '''
  Run the pipeline immediately, then again after every_minutes.

  A failed run is logged. The loop keeps the next appointment.
  KeyboardInterrupt stops the loop.
  '''
  while True:
    try:
      runner()
    except KeyboardInterrupt:
      raise
    except Exception as error:
      logger.error(f'Scheduled run failed: {error}')
    logger.info(f'Next run in {every_minutes} minute(s)')
    try:
      sleep(every_minutes * 60)
    except KeyboardInterrupt:
      logger.info('Scheduler stopped')
      return
