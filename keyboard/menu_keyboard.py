from pyrogram.types import (
    KeyboardButton, ReplyKeyboardMarkup
)

from . import buttons

MENU_BUTTON = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons.PROFILE_BUTTON),
            KeyboardButton(text=buttons.USER_STATISTICS_BUTTON)
        ],
        [
            KeyboardButton(text=buttons.CONTROL_BUTTON),
            KeyboardButton(text=buttons.SETTING_BUTTON)
        ]
    ],
    resize_keyboard=True
)
SETTINGS_BUTTON = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons.SETTING_TIME_ZONE_BUTTON),
            KeyboardButton(text=buttons.SETTING_NOTIFICATIONS_BUTTON)
        ],
        [
            KeyboardButton(text=buttons.BACK_BUTTON)

        ]
    ],
    resize_keyboard=True
)
SETTINGS_NOTIFICATIONS = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons.SETTING_REMINDER_TIME_BUTTON)

        ],
        [
            KeyboardButton(text=buttons.BACK_BUTTON)

        ]
    ],
    resize_keyboard=True
)
CONTROL_BUTTON = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=buttons.CONTROL_PIN_BUTTON),
            KeyboardButton(text=buttons.CONTROL_GROUPS_BUTTON),
            KeyboardButton(text=buttons.CONTROL_USERS_BUTTON)

        ],
        [
            KeyboardButton(text=buttons.BACK_BUTTON)

        ]
    ],
    resize_keyboard=True
)