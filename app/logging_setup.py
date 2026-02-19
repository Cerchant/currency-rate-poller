import logging
import sys

from app.config import settings


def setup_logging() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    root_logger.addHandler(stdout_handler)

    file_handler = logging.FileHandler("errors.log")
    file_handler.setLevel(logging.ERROR)
    root_logger.addHandler(file_handler)
