from pyrogram.types import (
    KeyboardButton, ReplyKeyboardMarkup
)

from . import markup_buttons

MENU_kEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=markup_buttons.PROFILE_BUTTON)
        ],
        [
            KeyboardButton(text=markup_buttons.CONTROL_BUTTON),
            KeyboardButton(text=markup_buttons.SETTING_BUTTON)
        ]
    ],
    resize_keyboard=True
)
SETTINGS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=markup_buttons.SETTING_TIME_ZONE_BUTTON),
            KeyboardButton(text=markup_buttons.SETTING_NOTIFICATIONS_BUTTON)
        ],
        [
            KeyboardButton(text=markup_buttons.BACK_BUTTON)

        ]
    ],
    resize_keyboard=True
)
SETTINGS_NOTIFICATIONS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=markup_buttons.SETTING_LIST_BUTTON),
            KeyboardButton(text=markup_buttons.SETTING_REMINDER_TIME_BUTTON)
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
            KeyboardButton(text=markup_buttons.CONTROL_GROUPS_BUTTON),
            KeyboardButton(text=markup_buttons.CONTROL_USERS_BUTTON)

        ],
        [
            KeyboardButton(text=markup_buttons.BACK_BUTTON)

        ]
    ],
    resize_keyboard=True
)