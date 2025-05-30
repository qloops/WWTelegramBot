from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboards


@bot.bot.on_message(filters.regex(f"^{keyboards.markup_buttons.SETTING_BUTTON}$"))
async def settings_button(client: Client, message: Message):
    await message.reply(
        "Настройки.", 
        reply_markup=keyboards.markup_keyboards.SETTINGS_KEYBOARD
    )