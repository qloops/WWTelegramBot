from typing import List
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import constants
import database

def create_timezone_keyboard(buttons_per_row: int = 4) -> InlineKeyboardMarkup:
    timezones = list(constants.TIMEZONES.keys())
    timezones.reverse()
    buttons = []
    for i in range(0, len(timezones), buttons_per_row):
        row = [
            InlineKeyboardButton(
                text=tz, 
                callback_data=f"set_timezone_{tz}"
            ) 
            for tz in timezones[i:i + buttons_per_row]
        ]
        buttons.append(row)
    
    return InlineKeyboardMarkup(buttons)