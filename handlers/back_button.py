import re

from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboard


@bot.bot.on_message(filters.regex(f"^{keyboard.buttons.BACK_BUTTON}$"))
async def back_command(client: Client, message: Message):
    await message.reply("/", reply_markup=keyboard.menu_keyboard.MENU_BUTTON)