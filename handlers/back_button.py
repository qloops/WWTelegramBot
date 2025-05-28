from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboards


@bot.bot.on_message(filters.regex(f"^{keyboards.markup_buttons.BACK_BUTTON}$"))
async def back_button(client: Client, message: Message):
    await message.reply("/", reply_markup=keyboards.markup_keyboards.MENU_KEYBOARD)