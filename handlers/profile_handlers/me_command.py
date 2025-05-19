from pyrogram import (
    Client, 
    filters
)
from pyrogram.types import Message

import bot
import keyboards
import database
import views
import constants


@bot.bot.on_message(
    filters.regex(f"^{keyboards.markup_buttons.PROFILE_BUTTON}$") |
    filters.command("me")
)
async def profile_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_profile=database.db_interface.users_profiles.find_one(
        condition={"user_id": user_id}
    )

    if not user_profile:
        await message.reply(text=constants.messages.COULDNT_FIND_A_PROFILE)
    else:
        await message.reply(
            text=views.UserProfileFormatter.to_user_message(user_profile)
        )