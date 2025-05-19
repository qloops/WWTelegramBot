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
    filters.regex(f"^{keyboards.markup_buttons.CONTROL_BUTTON}$")
)
async def control_button(client: Client, message: Message):
    user_id = message.from_user.id
    
    user = database.db_interface.users.find_one(condition={"user_id": user_id})
    if not utils.access_check(user, constants.UserAccessRoles.CHAPTER):
        await message.reply(constants.messages.NO_ACCESS)
        return
    else:
        await message.reply(
            "Управление.", 
            reply_markup=keyboards.markup_keyboards.CONTROL_KEYBOARD
        )