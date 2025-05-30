import os
import logging

import logs
from dotenv import load_dotenv

load_dotenv()

logs.configure_logging(
    console_level=getattr(logging, os.getenv("CONSOLE_LOG_LEVEL", "ERROR")),
    file_level=getattr(logging, os.getenv("FILE_LOG_LEVEL", "INFO"))
)

from pyrogram import idle

import handlers
from bot import bot

from __init__ import __version__

logger = logging.getLogger(__name__)


async def main():
    try:
        await bot.start()
        logger.info(
            f"Bot @{bot.me.username} V{__version__} started!"
        )
        await idle()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise
    finally:
        await bot.stop()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    bot.run(main())