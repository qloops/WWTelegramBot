from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboards
import database

@bot.bot.on_message(filters.regex(f"^{keyboards.markup_buttons.SETTING_BUTTON}$"))
async def settings_button(client: Client, message: Message):
    user_id = message.from_user.id
    if not database.db_interface.users_settings.exists(condition={"user_id": user_id}):
        database.db_interface.users_settings.insert_one(database.models.UserSettings(user_id=user_id))
    await message.reply("/", reply_markup=keyboards.markup_keyboards.SETTINGS_KEYBOARD)