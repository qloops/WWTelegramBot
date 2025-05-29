from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType

import bot
import keyboards
import database


@bot.bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    if not database.db_interface.users.exists(condition={"user_id": user_id}):
        database.db_interface.users.insert_one(database.models.User(user_id=user_id))
    
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(text="Салам! Скинь профиль.", reply_markup=keyboards.markup_keyboards.MENU_KEYBOARD)
    else:
        await message.reply(text="Салам!")