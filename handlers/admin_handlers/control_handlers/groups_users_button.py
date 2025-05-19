import re

from pyrogram import (
    Client, 
    filters
)
from pyrogram.types import Message

import bot
import keyboards
import utils
import database
import constants


@bot.bot.on_message(
    filters.regex(
        f"^{keyboards.markup_buttons.CONTROL_SETTING_GROUPS_USERS_BUTTON}$"
    )
)
async def setting_groups_users_button(client: Client, message: Message):
    user_id = message.from_user.id
    
    user = database.db_interface.users.find_one(condition={"user_id": user_id})
    if not utils.access_check(user, constants.UserAccessRoles.ADMINISTRATOR):
        await message.reply(constants.messages.NO_ACCESS)
        return

    await message.reply(
        # TODO: Here you need a groups profile.
        text=".", 
        reply_markup=keyboards.inline_keyboards.USERS_GROUP_KEYBOARD
    )


@bot.bot.on_message(
    filters.regex(re.compile(r"^/create_group\s(?P<attribute>.+)$"), re.I)
)
async def сreate_group_command(client: Client, message: Message):
    user_id = message.from_user.id
    attribute = message.matches[0].group("attribute")

    user = database.db_interface.users.find_one(condition={"user_id": user_id})
    if not utils.access_check(user, constants.UserAccessRoles.ADMINISTRATOR):
        await message.reply(constants.messages.NO_ACCESS)
        return

    if database.db_interface.users_groups.exists(
        condition={"group_name": attribute}
    ):
        await message.reply(text="Такая группа уже существует.")
        return
    
    database.db_interface.users_groups.insert_one(
        database.models.UsersGroup(group_name=attribute)
    )
    # TODO: A specific group profile is needed here.
    await message.reply(constants.messages.SUCCESSFULLY)


@bot.bot.on_message(
    filters.regex(re.compile(r"^/open_group\s(?P<attribute>.+)$"), re.I)
)
async def сreate_group_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    user = database.db_interface.users.find_one(condition={"user_id": user_id})
    if not utils.access_check(user, constants.UserAccessRoles.CHAPTER):
        await message.reply(constants.messages.NO_ACCESS)
        return

    await utils.send_cached_photo(
        chat_id=message.chat.id, 
        file_name="technical_work.png", 
        caption="🪛⚙️ Technical work"
    )