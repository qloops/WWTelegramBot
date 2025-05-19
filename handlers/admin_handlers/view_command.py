import os
import re

from pyrogram import (
    Client, 
    filters
)
from pyrogram.types import Message
from pyrogram.enums import ChatType

import bot
import constants
import database
import views
import utils
import keyboards


@bot.bot.on_message(
    filters.reply &
    filters.command("view")
)
async def view_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    user = database.db_interface.users.find_one(condition={"user_id": user_id})
    if not utils.access_check(
        user=user, 
        role=constants.UserAccessRoles.CHAPTER
    ):
        await message.reply(constants.messages.NO_ACCESS)
        return

    reply_user_id = message.reply_to_message.from_user.id
    reply_user_profile = database.db_interface.users_profiles.find_one(
        condition={"user_id": reply_user_id}
    )

    if not reply_user_profile:
        await message.reply(constants.messages.COULDNT_FIND_A_PROFILE)
        return

    await message.reply(
        views.formatters.UserProfileFormatter.to_admin_message(
            user_profile=reply_user_profile, 
            admin_id=user_id
        )
    )


@bot.bot.on_message(
    filters.regex(
        re.compile(
            rf"^/view_(?P<user_id>\d+)({os.environ.get('BOT_USERNAME')})?$", 
            re.IGNORECASE
        )
    )
)
async def view_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    user = database.db_interface.users.find_one(condition={"user_id": user_id})
    if not utils.access_check(
        user=user, role=constants.UserAccessRoles.CHAPTER
    ):
        await message.reply(constants.messages.NO_ACCESS)
        return

    reply_user_id = int(message.matches[0].group("user_id"))
    reply_user_profile = database.db_interface.users_profiles.find_one(
        condition={"user_id": reply_user_id}
    )
    reply_user = database.db_interface.users.find_one(
        condition={"user_id": reply_user_id}
    )

    if not reply_user or not reply_user_profile:
        await message.reply(constants.messages.COULDNT_FIND_A_PROFILE)
        return

    keyboard = None
    if message.chat.type == ChatType.PRIVATE:
        keyboard = keyboards.builders.create_admin_settings_user_keyboard(
            reply_user
        )

    await message.reply(
        text=views.formatters.UserProfileFormatter.to_admin_message(
            user_profile=reply_user_profile, 
            admin_id=user_id
        ),
        reply_markup=keyboard
    )