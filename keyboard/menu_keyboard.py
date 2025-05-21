from pyrogram.types import (
    KeyboardButton, ReplyKeyboardMarkup
)

MENU_BUTTON = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Профиль"),
            KeyboardButton(text="Настройки"),
            KeyboardButton(text="Управление")
        ],
    ],
    resize_keyboard=True
)