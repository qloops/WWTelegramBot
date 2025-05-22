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


SETTINGS_BUTTON = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Изменить часоовой пояс"),
            KeyboardButton(text="Изменить секунды до напоминания"),
            KeyboardButton(text="Назад")

        ],
    ],
    resize_keyboard=True
)


CONTROL_BUTTON = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пин"),
            KeyboardButton(text="Настройка групп"),
            KeyboardButton(text="Настройка пользователей"),
            KeyboardButton(text="Назад")

        ],
    ],
    resize_keyboard=True
)