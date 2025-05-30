from datetime import datetime, timezone

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import MessageNotModified

import bot
import keyboards
import database
import views

@bot.bot.on_callback_query(filters.regex(r"^set_timezone_(?P<time_zone>[+-]\d+:\d+)$"))
async def setting_time_zone_callback(client: Client, call: CallbackQuery):
    user_id = call.from_user.id
    callback_data = call.matches[0].group("time_zone")

    database.db_interface.users_settings.update_timezone(
        user_id=user_id, 
        timezone_str=callback_data
    )

    user_settings = database.db_interface.users_settings.find_one(condition={"user_id": user_id})
    
    try:
        await call.message.edit(
            views.UserSettingsFormatter.to_local_user_time(user_settings), 
            reply_markup=keyboards.inline_keyboards.TIME_ZONE_KEYBOARD
        )
    except MessageNotModified:
        pass 
    await call.answer("Успешно.")


@bot.bot.on_message(filters.regex(f"^{keyboards.markup_buttons.SETTING_TIME_ZONE_BUTTON}$"))
async def time_zone_button(client: Client, message: Message):
    user_id = message.from_user.id
    user_settings = database.db_interface.users_settings.find_one(condition={"user_id": user_id})

    await message.reply(
        views.UserSettingsFormatter.to_local_user_time(user_settings), 
        reply_markup=keyboards.inline_keyboards.TIME_ZONE_KEYBOARD
    )