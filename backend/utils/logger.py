import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logger
logger = logging.getLogger('phishshield')
logger.setLevel(logging.INFO)

# Create formatters and handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File Handler (max 5MB per file, keep 5 backup files)
file_handler = RotatingFileHandler(
    'logs/phishshield.log',
    maxBytes=5*1024*1024,  # 5MB
    backupCount=5
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create error logger specifically for tracking errors
error_logger = logging.getLogger('phishshield.error')
error_logger.setLevel(logging.ERROR)

# Error log file handler
error_file_handler = RotatingFileHandler(
    'logs/error.log',
    maxBytes=5*1024*1024,
    backupCount=5
)
error_file_handler.setFormatter(formatter)
error_logger.addHandler(error_file_handler)
error_logger.addHandler(console_handler)  # Also show errors in console

def log_error(error, additional_info=None):
    """
    Log an error with optional additional context
    """
    if additional_info:
        error_logger.error(f"{str(error)} - Additional Info: {additional_info}")
    else:
        error_logger.error(str(error))
