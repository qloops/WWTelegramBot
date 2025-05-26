import re

from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboard
# from database.database import db_interface as db
# from database.models import User

@bot.bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    # user = User(
    #     id= message.from_user.id
    # )
    # if not db.get_user({"id": user.id}):
    #     db.insert_user(user)

    await message.reply(text="Салам! Скинь профиль.", reply_markup=keyboard.menu_keyboard.MENU_BUTTON)