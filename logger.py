import logging

def setup_logger():
  '''
  Sets up a logger for the ETL pipeline.

  The logger writes log messages to a file named 'etl_pipeline.log' with a specific format
  that includes the timestamp, log level, and message.

  Returns:
    logging.Logger: Configured logger instance.
  '''
  # Create a logger with the name 'ETL_Pipeline'
  logger = logging.getLogger("ETL_Pipeline")
  
  # Create a file handler to write logs to 'etl_pipeline.log'
  handler = logging.FileHandler("etl_pipeline.log")
  handler.setLevel(logging.INFO)  # Set the logging level to INFO

  # Define the log message format
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)  # Apply the formatter to the handler

  # Add the handler to the logger
  logger.addHandler(handler)
  
  return logger

# Initialize the logger
logger = setup_logger()