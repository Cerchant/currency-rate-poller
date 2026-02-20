import logging
import sys

from app.config import settings

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATEFMT)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(formatter)
    root_logger.addHandler(stdout_handler)

    file_handler = logging.FileHandler("errors.log")
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
