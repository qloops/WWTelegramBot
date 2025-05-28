from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)

from . import inline_buttons


INLINE_NOTIFICATIONS_SETTIТNG_BUTTON = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=inline_buttons.INLINE_SETTING_PIN_NOTIFICATIONS, callback_data="switch_setting_pin_notification")
        ]
    ]
)