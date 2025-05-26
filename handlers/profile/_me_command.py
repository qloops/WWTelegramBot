# import re

# from pyrogram import Client, filters
# from pyrogram.types import Message

# import bot
# from database.database import db_interface as db


# @bot.bot.on_message(filters.regex(re.compile("^Профиль$", re.I)) | filters.command("me"))
# async def profile_command(client: Client, message: Message):
#     user_id = message.from_user.id
#     user_profile=db.get_user_profile({"id": user_id})

#     if user_profile:
#         await message.reply_text(user_profile.get_formatted_profile())
#     else:
#         await message.reply_text("Не нашел твоего профиля у себя в базе")
