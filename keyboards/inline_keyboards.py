from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)

from . import inline_buttons
from . import builders

NOTIFICATIONS_SETTITNG_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=inline_buttons.PIN_NOTIFICATIONS_BUTTON, 
                callback_data="toggle_setting_pin_notification"
            )
        ]
    ]
)
TIME_ZONE_KEYBOARD = builders.create_timezone_keyboard(buttons_per_row=4)
USERS_GROUP_KEYBOARD = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=inline_buttons.SHOW_LIST_USERS_GROUPS, 
                    switch_inline_query_current_chat=f"Groups: View: "
                )
            ],
            [
                InlineKeyboardButton(
                    text=inline_buttons.CREATE_USERS_GROUPS, 
                    switch_inline_query_current_chat=f"Groups: Create: "
                )
            ]
        ]
    )