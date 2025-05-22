import re

from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboard
from database.database import db_interface as db


@bot.bot.on_message(filters.regex(re.compile("^Управление$", re.I)))
async def control_command(client: Client, message: Message):
    await message.reply("/", reply_markup=keyboard.CONTROL_BUTTON)