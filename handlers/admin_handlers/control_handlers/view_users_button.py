import re

from pyrogram import (
    Client, 
    filters
)
from pyrogram.types import Message

import bot
import keyboards
import keyboards.builders
import utils
import database
import constants


@bot.bot.on_message(
    filters.regex(f"^{keyboards.markup_buttons.CONTROL_VIEW_USERS_BUTTON}$")
)
async def view_users_button(client: Client, message: Message):
    user_id = message.from_user.id
    
    user = database.db_interface.users.find_one(condition={"user_id": user_id})
    if not utils.access_check(
        user=user, 
        role=constants.UserAccessRoles.CHAPTER
    ):
        await message.reply(constants.messages.NO_ACCESS)
        return
    
    unique_fields_gang = (
        database.db_interface.users_profiles.get_unique_gangs_names()
    )
    await message.reply(
        text="Просмотр пользователей.",
        reply_markup=(
            keyboards.builders.create_view_gangs_keyboard(unique_fields_gang)
        )
    )


@bot.bot.on_message(
        filters.regex(re.compile(r"🔍\s(?P<gang_name>.+)", re.IGNORECASE))
)
async def view_gang_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    user = database.db_interface.users.find_one(condition={"user_id": user_id})
    if not utils.access_check(user, constants.UserAccessRoles.CHAPTER):
        await message.reply(constants.messages.NO_ACCESS)
        return
    
    gang_name = message.matches[0].group("gang_name") 
    if (
        gang_name not in 
        database.db_interface.users_profiles.get_unique_gangs_names()
    ):
        await message.reply("Такой не существует.")
        return

    users_list =  database.db_interface.users_profiles.find_many(
        condition={"gang_name": gang_name}
    )
    users_list = sorted(
        users_list, key=lambda user: user.stats_sum, reverse=True
    )
    sum_bm = sum(map(lambda user: user.stats_sum, users_list))

    text = f"БМ всего: <b>{sum_bm}</b>\n"
    for num, user in enumerate(users_list, 1):
        text += (
            f"{num}. {user.nickname}\n🏵: <b>{user.zen}</b> | БМ: "
            f"<b>{user.stats_sum}</b> — /view_{user.user_id}\n\n"
        )
    await message.reply(text)