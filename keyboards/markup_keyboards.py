from pyrogram.types import (
    KeyboardButton, 
    ReplyKeyboardMarkup
)

from . import markup_buttons

MENU_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=markup_buttons.PROFILE_BUTTON),
            KeyboardButton(text=markup_buttons.SETTING_BUTTON)
        ],
        [
            KeyboardButton(text=markup_buttons.CONTROL_BUTTON),
        ]
    ],
    resize_keyboard=True
)
SETTINGS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=markup_buttons.SETTING_NOTIFICATIONS_BUTTON),
            KeyboardButton(text=markup_buttons.SETTING_TIME_ZONE_BUTTON)

        ],
        [
            KeyboardButton(text=markup_buttons.BACK_BUTTON)
        ]
    ],
    resize_keyboard=True
)
CONTROL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=markup_buttons.CONTROL_PIN_BUTTON),
        ],
        [
            KeyboardButton(text=markup_buttons.CONTROL_SETTING_GROUPS_USERS_BUTTON),
            KeyboardButton(text=markup_buttons.CONTROL_VIEW_USERS_BUTTON)
        ],
        [
            KeyboardButton(text=markup_buttons.BACK_BUTTON)

        ]
    ],
    resize_keyboard=True
)