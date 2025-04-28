import logging

def setup_logger():
  '''
  Sets up a logger for the ETL pipeline.

  The logger writes log messages to a file named 'etl_pipeline.log' with a specific format
  that includes the timestamp, log level, and message.
  The logger also prints log messages to the console.

  Returns:
      logging.Logger: Configured logger instance.
  '''
  # Create a logger with the name 'ETL_Pipeline'
  logger = logging.getLogger("ETL_Pipeline")
  
  # Set the global log level (this will affect all handlers)
  logger.setLevel(logging.DEBUG)  # Set the level to DEBUG to capture all log levels

  # File handler to write logs to 'etl_pipeline.log'
  file_handler = logging.FileHandler("etl_pipeline.log")
  file_handler.setLevel(logging.INFO)  # Set the logging level to INFO for the file handler

  # Console handler to print logs to terminal (console)
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.DEBUG)  # Set the logging level to DEBUG for the console handler

  # Define the log message format
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  file_handler.setFormatter(formatter)  # Apply the formatter to the file handler
  console_handler.setFormatter(formatter)  # Apply the formatter to the console handler

  # Add the handlers to the logger
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
  
  return logger

# Initialize the logger
logger = setup_logger()