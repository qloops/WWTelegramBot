from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton
)

import utils


def create_timezone_keyboard(timezones_dict, buttons_in_row=3):
    buttons = []
    row = []
    for i, key in enumerate(timezones_dict.keys(), start=1):
        button = InlineKeyboardButton(text=key, callback_data=key)
        row.append(button)
        if i % buttons_in_row == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


TIME_ZONE_INLINE_BUTTON = create_timezone_keyboard(utils.get_time_zone.timezones)