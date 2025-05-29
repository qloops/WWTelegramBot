import os
import logging
from .builders import create_forwarded_from_filter


class GameBotForwarded:
    BOT_WW_ID = int(os.environ["BOT_WW_ID"])

    def __new__(cls):
        return create_forwarded_from_filter(cls.BOT_WW_ID)