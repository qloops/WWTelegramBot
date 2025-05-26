import re

from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboard


@bot.bot.on_message(filters.regex(re.compile(f"^{keyboard.buttons.CONTROL_BUTTON}$")))
async def control_button(client: Client, message: Message):
    await message.reply("/", reply_markup=keyboard.menu_keyboard.CONTROL_BUTTON)