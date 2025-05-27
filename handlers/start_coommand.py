from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType

import bot
import keyboard
import database


@bot.bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    if not database.db_interface.users.exists(condition={"id": user_id}):
        database.db_interface.users.insert_one(database.models.User(user_id))
    
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(text="Салам! Скинь профиль.", reply_markup=keyboard.menu_keyboard.MENU_BUTTON)
    else:
        await message.reply(text="Салам!")
