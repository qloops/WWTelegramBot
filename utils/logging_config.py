import logging
import sys

def configure_logging(level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
