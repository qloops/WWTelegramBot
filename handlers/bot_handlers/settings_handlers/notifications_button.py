from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import MessageNotModified

import bot
import keyboards
import database
import views

CHECK_MARK = "✅"
CROSS_MARK = "❌"


@bot.bot.on_callback_query(filters.regex(r"^toggle_setting_(?P<setting_name>.+)$"))
async def toggle_settings_callback(client: Client, call: CallbackQuery):
    user_id = call.from_user.id
    setting_name = call.matches[0].group("setting_name")

    success, new_value = database.db_interface.users_settings.toggle_boolean_setting(
        user_id=user_id, 
        setting_name=setting_name
    )

    if success:
        user_settings = database.db_interface.users_settings.find_one({"user_id": user_id})

        try:
            await call.message.edit(
                views.UserSettingsFormatter.to_notifications_message(user_settings),
                reply_markup=keyboards.inline_keyboards.NOTIFICATIONS_SETTITNG_KEYBOARD
            )
        except MessageNotModified:
            pass

    await call.answer("Успешно.")


@bot.bot.on_message(filters.regex(f"^{keyboards.markup_buttons.SETTING_NOTIFICATIONS_BUTTON}$"))
async def notifications_button(client: Client, message: Message):
    user_id = message.from_user.id
    user_settings = database.db_interface.users_settings.find_one(condition={"user_id": user_id})

    await message.reply(
        views.UserSettingsFormatter.to_notifications_message(user_settings), 
        reply_markup=keyboards.inline_keyboards.NOTIFICATIONS_SETTITNG_KEYBOARD
    )