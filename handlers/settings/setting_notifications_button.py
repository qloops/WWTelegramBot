from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.errors import MessageNotModified

import bot
import keyboard
import database

def get_settings_string(settings: database.models.UserSettings) -> str:
    CHECK_MARK = "✅"
    CROSS_MARK = "❌"
    
    notify_pin_status_emoji = CHECK_MARK if settings.pin_notification else CROSS_MARK
    
    return f"{notify_pin_status_emoji} Уведомление о рейде."


@bot.bot.on_callback_query(filters.regex(r"^switch_setting_(?P<settings_type>.+)$"))
async def switch_setting_callback(client: Client, call: CallbackQuery):
    user_id = call.from_user.id
    settings_type = call.matches[0].group("settings_type")
    
    success, _ = database.db_interface.users_settings.toggle_boolean_setting(
        user_id, 
        settings_type
    )

    if success:
        user_settings = database.db_interface.users_settings.find_one({"id": user_id})
    
        try:
            await call.message.edit(
                get_settings_string(user_settings), 
                reply_markup=keyboard.inline_keyboards.INLINE_NOTIFICATIONS_SETTIТNG_BUTTON
            )
        except MessageNotModified:
            pass
        
    await call.answer("Успешно.", show_alert=True)



@bot.bot.on_message(filters.regex(f"^{keyboard.markup_buttons.SETTING_LIST_BUTTON}$"))
async def setting_list_button(client: Client, message: Message):
    user_id = message.from_user.id
    user_settigs = database.db_interface.users_settings.find_one(condition={"id": user_id})

    await message.reply(get_settings_string(user_settigs), reply_markup=keyboard.inline_keyboards.INLINE_NOTIFICATIONS_SETTIТNG_BUTTON)