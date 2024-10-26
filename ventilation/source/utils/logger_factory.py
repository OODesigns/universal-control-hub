import logging
import logging.handlers
import os
from dataclasses import dataclass
from datetime import datetime

# Best practice settings
LOG_DIR = 'logs'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_LEVEL = logging.DEBUG

@dataclass
class LoggerResponse:
    logger: logging.Logger
    filename: str

class LoggerFactory:

    """Class to create and configure loggers."""
    @classmethod
    def get_logger(cls, name) -> LoggerResponse:
        # Ensure log directory exists
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        # Creating a unique log file for each run
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(LOG_DIR, f'{name}_{current_time}.log')

        # Setting up logging configuration
        log_instance = logging.getLogger(name)
        log_instance.setLevel(LOG_LEVEL)

        # Formatter setup
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        # File handler setup
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(LOG_LEVEL)

        # Stream handler setup (for console output)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.ERROR)

        # Avoid adding multiple handlers in case the log_instance already has them
        if not log_instance.hasHandlers():
            log_instance.addHandler(file_handler)
            log_instance.addHandler(console_handler)

        # Attach the log file path to the log_instance for later use
        log_instance.__log_file = log_file

        return LoggerResponse(log_instance, log_file)

# Usage example
if __name__ == "__main__":
    app_logger = LoggerFactory.get_logger("MyAppLogger")
    try:
        app_logger.logger.info("Application started")
        # Simulate some operations
        x = 1 / 0  # Intentional error for demonstration
    except Exception as e:
        app_logger.logger.error("An error occurred: %s", str(e), exc_info=True)
    finally:
        app_logger.logger.info("Application finished")
        print(f"Log file created: {app_logger.filename}")
