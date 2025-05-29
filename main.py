import os
import logging

import logs
from dotenv import load_dotenv

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO")
logs.configure_logging(getattr(logging, log_level))

from pyrogram import idle

import handlers
from bot import bot

from __init__ import __version__

logger = logging.getLogger(__name__)


async def main():
    try:
        await bot.start()
        logger.info(
            f"Bot @{bot.me.username} started successfully!\n"
            f"Bot version: {__version__}"
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