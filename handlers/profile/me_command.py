import re

from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboards
import database

@bot.bot.on_message(filters.regex(f"^{keyboards.markup_buttons.PROFILE_BUTTON}$") | filters.command("me"))
async def profile_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_profile=database.db_interface.users_profiles.find_one(condition={"id": user_id})

    if not user_profile:
        await message.reply("Не удалось найти профиль.")
    else:
        await message.reply(user_profile.get_formatted_profile_string())