import os

from pyrogram import (
    Client,
    filters
)
from pyrogram.types import Message
from pyrogram.enums import ChatType

import bot
import rules
import constants


@bot.bot.on_message(rules.user_banned)
async def banned_handler(client: Client, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(text=constants.messages.PLACEHOLDER_BANNED)
    elif (
        message.reply_to_message and
        message.reply_to_message.from_user.id == os.environ.get("BOT_WW_ID")
    ):
        await message.reply(text=constants.messages.PLACEHOLDER_BANNED)
    return


@bot.bot.on_message(
    rules.empty_profle &
    ~filters.regex(constants.patterns.ProfilePatterns.FULL_PROFILE) &
    ~filters.regex(constants.patterns.ProfilePatterns.SHORT_PROFILE)
)
async def empty_profile_handler(client: Client, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(text=constants.messages.EMPTY_PROFILE)
    elif (
        message.reply_to_message and
        message.reply_to_message.from_user.id == os.environ.get("BOT_WW_ID")
    ):
        await message.reply(text=constants.messages.EMPTY_PROFILE)
    return