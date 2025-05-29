import logging
import sys
import os
from logging.handlers import RotatingFileHandler


def configure_logging(console_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(log_dir, "bot.log")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info(f"Logging configured: console level={logging.getLevelName(console_level)}, file level=DEBUG")