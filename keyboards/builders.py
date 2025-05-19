from typing import List
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

import constants
import database
from . import markup_buttons
from . import inline_buttons

def create_timezone_keyboard(buttons_per_row: int) -> InlineKeyboardMarkup:
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


def create_view_gangs_keyboard(buttons_list: List[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"🔍 {button}")] for button in buttons_list] + 
            [[KeyboardButton(text=markup_buttons.BACK_BUTTON)]],
        resize_keyboard=True
    )


def create_admin_settings_user_keyboard(
        user: database.models.User
) -> InlineKeyboardMarkup:
    chapter_status_emoji = (
        constants.messages.CHECK_MARK 
        if user.access_level == constants.UserAccessRoles.CHAPTER.value
        else constants.messages.CROSS_MARK
    )
    banned_status_emoji = (              
        constants.messages.CHECK_MARK 
        if user.banned 
        else constants.messages.CROSS_MARK
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=inline_buttons.USER_BANNED_BUTTON.format(
                        banned_status_emoji
                    ),
                    callback_data=(
                        f"admin_change_user_banned_{user.user_id}"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text=inline_buttons.USER_CHAPTER_BUTTON.format(
                        chapter_status_emoji
                    ),
                    callback_data=f"admin_change_user_chapter_{user.user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=inline_buttons.DELETE_FROM_GANG_BUTTON,
                    callback_data=f"remove_user_from_gang_{user.user_id}"
                )
            ]
        ]
    )


def confirm_deletion_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=inline_buttons.YES_DELETION_BUTTON, 
                    callback_data=f"yes_delete_{user_id}"
                ),
                InlineKeyboardButton(
                    text=inline_buttons.NO_DELETION_BUTTON, 
                    callback_data=f"no_delete_{user_id}"
                )
            ]
        ]
    )