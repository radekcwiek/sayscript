import logging
from logging.handlers import RotatingFileHandler

from app.platform_paths import ensure_app_dirs, get_log_dir
from app.version import APP_NAME


LOGGER_NAME = APP_NAME.lower().replace(" ", "-")


def setup_logging() -> logging.Logger:
    ensure_app_dirs()

    log_file = get_log_dir() / f"{LOGGER_NAME}.log"

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

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

    return logger


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)
