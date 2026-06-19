# SPDX-License-Identifier: Apache-2.0

"""
Logging setup for SayScript.

This module configures one application-wide logger with a rotating log file.
Other modules should not configure logging themselves. They should call
get_logger() and use the shared SayScript logger.

The log file location is provided by app.platform_paths, so it works on both
Windows and Linux.
"""

import logging
from logging.handlers import RotatingFileHandler

from app.platform_paths import ensure_app_dirs, get_log_dir
from app.version import APP_NAME


# Logger name used throughout the application.
# Example: "SayScript" -> "sayscript"
LOGGER_NAME = APP_NAME.lower().replace(" ", "-")


def setup_logging() -> logging.Logger:
    """
    Configure and return the application logger.

    This function is meant to be called once during application startup.
    It is safe to call multiple times because it checks whether handlers
    already exist before adding a new file handler.
    """
    ensure_app_dirs()

    log_file = get_log_dir() / f"{LOGGER_NAME}.log"

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    # Prevent messages from being passed to the root logger.
    # This avoids duplicate log output if another library configures logging.
    logger.propagate = False

    # If setup_logging() was already called, do not add another handler.
    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Logging initialized: %s", log_file)

    return logger


def get_logger() -> logging.Logger:
    """
    Return the shared SayScript logger.

    setup_logging() should be called during application startup before this
    logger is used extensively. If it has not been called yet, this still
    returns a valid logger object, but it may not have a file handler yet.
    """
    return logging.getLogger(LOGGER_NAME)
