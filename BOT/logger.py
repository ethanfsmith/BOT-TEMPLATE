"""
Logger Configuration
------------------------------------

Copyright © 2023

Description:
    This module configures the logger, providing a centralized logging system
    for recording events, errors, and information related to the bot's execution. The logger is configured
    to output log messages to both the console with ANSI color-coded formatting and a rotating file
    to maintain historical logs.

Author:
    Ethan Smith

Usage:
    Import this module in your main script and call the 'setup_logging' function to initialize the logger.
    The logger is set to log messages with a specified format and color-coded levels to enhance readability.
    Log files are stored in the 'LOG' directory at the BOT TEMPLATE level.

Configuration:
    - ANSI color codes are used for console log formatting to distinguish log levels.
    - RotatingFileHandler is employed to manage log files, ensuring a maximum size and backup log retention.

Log Levels:
    - DEBUG: Lime Green
    - INFO: Light Blue
    - WARNING: Yellow
    - ERROR: Red
    - CRITICAL: Blood Red

Note:
    Adjust the log levels and formatting as needed for your specific use case. Ensure that the 'LOG' directory
    is created at the BOT TEMPLATE level to store log files.

"""
import logging
from logging.handlers import RotatingFileHandler
import os

# Define ANSI color codes
class LogColors:
    DEBUG = '\033[92m'  # Lime Green
    INFO = '\033[94m'   # Light Blue
    WARNING = '\033[93m'  # Yellow
    ERROR = '\033[91m'   # Red
    CRITICAL = '\033[38;2;139;0;0m'  # Blood Red
    RESET = '\033[0m'    # Reset to default

# Custom Formatter
class ColorFormatter(logging.Formatter):
    FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s (%(filename)s:%(lineno)d)"

    COLOR_MAP = {
        logging.DEBUG: LogColors.DEBUG,
        logging.INFO: LogColors.INFO,
        logging.WARNING: LogColors.WARNING,
        logging.ERROR: LogColors.ERROR,
        logging.CRITICAL: LogColors.CRITICAL,
    }

    def format(self, record):
        log_fmt = self.COLOR_MAP.get(record.levelno) + self.FORMAT + LogColors.RESET
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logging():
    # Create LOG directory at the BOT TEMPLATE level
    log_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'LOG')
    os.makedirs(log_directory, exist_ok=True)

    # Setup logger
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)  # Set this to the lowest level you want to log

    # Create a rotating file handler
    log_file = os.path.join(log_directory, 'discord.log')
    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8', mode='a')
    handler.setFormatter(ColorFormatter())
    
    # Add the handler to the logger
    logger.addHandler(handler)

    return logger