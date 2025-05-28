from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import MessageNotModified

import bot
import keyboard
import database


@bot.bot.on_callback_query(filters.regex(r"^[+-]\d+:\d+$"))
async def setting_time_zone_callback(client: Client, call: CallbackQuery):
    user_id = call.from_user.id
    callback_data = call.data

    database.db_interface.users_settings.update_timezone(
        condition={"id": user_id}, 
        timezone_str=callback_data
    )
    user_settings = database.db_interface.users_settings.find_one(condition={"id": user_id})

    try:
        await call.message.edit(user_settings.time_zone, reply_markup=keyboard.time_zone_keyboard.TIME_ZONE_INLINE_BUTTON)
    except MessageNotModified:
        pass 
    await call.answer("Успешно.", show_alert=True)


@bot.bot.on_message(filters.regex(f"^{keyboard.markup_buttons.SETTING_TIME_ZONE_BUTTON}$"))
async def setting_time_zone_button(client: Client, message: Message):
    user_id = message.from_user.id
    user_settigs = database.db_interface.users_settings.find_one(condition={"id": user_id})
    await message.reply(user_settigs.time_zone, reply_markup=keyboard.time_zone_keyboard.TIME_ZONE_INLINE_BUTTON)