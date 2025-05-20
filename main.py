import logging

from utils.logging_config import configure_logging
from dotenv import load_dotenv

load_dotenv()
configure_logging(logging.ERROR)

from pyrogram import idle

import handlers
from bot import bot

logger = logging.getLogger(__name__)


async def main():
    await bot.start()
    await idle()
    await bot.stop()


if __name__ == '__main__':
    bot.run(main())