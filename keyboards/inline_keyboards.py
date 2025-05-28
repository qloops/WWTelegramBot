from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)

from . import inline_buttons
from . import builders


NOTIFICATIONS_SETTITNG_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=inline_buttons.PIN_NOTIFICATIONS_BUTTON, callback_data="switch_setting_pin_notification")
        ]
    ]
)
TIME_ZONE_KEYBOARD = builders.create_timezone_keyboard()