from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboard
import database

@bot.bot.on_message(filters.regex(f"^{keyboard.markup_buttons.SETTING_BUTTON}$"))
async def settings_button(client: Client, message: Message):
    user_id = message.from_user.id
    if not database.db_interface.users_settings.exists(condition={"id": user_id}):
        database.db_interface.users_settings.insert_one(database.models.UserSettings(id=user_id))
    await message.reply("/", reply_markup=keyboard.menu_keyboards.SETTINGS_KEYBOARD)