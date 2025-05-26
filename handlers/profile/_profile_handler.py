# import os
# import re
# import time

# from pyrogram import Client, filters
# from pyrogram.types import Message

# import bot
# from database.database import db_interface as db
# from database.models import FullUserProfile

# BOT_WW_ID = int(os.environ.get("BOT_WW_ID"))
# full_profile_regex = re.compile(
#     r"^📟Пип-бой\s3000\sv\d+\.\d+\n(Игровое\sсобытие\n\".+?\")?\n(?P<nickname>.+),\s(?P<emoji_fraction>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction_name>.+)\n🤟Банда:\s(?P<gang>.+)\n❤️Здоровье:\s\d+/(?P<max_hp>\d+)\n☠️Голод:\s\d+%\s/myfood\n⚔️Урон:\s(?P<damage>\d+)\s🛡Броня:\s(?P<armor>\d+)(\s\(\+\d+\))?\n{2}💪Сила:\s(?P<strength>\d+)\s🎯Меткость:\s(?P<accuracy>\d+)\n🗣Харизма:\s(?P<charisma>\d+)\s🤸🏽‍♂️Ловкость:\s(?P<dexterity>\d+)\n💡Умения\s/perks\n⭐️Испытания\s/warpass\n{2}🔋Выносливость:\s\d+/(?P<max_energy>\d+)\s/ref\n📍.+?, 👣\d+км\.\s\n{2}Экипировка:.+?(🏵(?P<zen>\d+)\s[▓░]+\n)?ID(?P<uid>\d+)",
#     re.S
# )


# def parse_pipboy_data(text: str, update_time: float):
#     match = full_profile_regex.search(text)
#     if not match:
#         return None

#     groups = match.groupdict()

#     return FullUserProfile(
#         update_time=update_time,
#         nickname=groups["nickname"],
#         emoji_fraction=groups["emoji_fraction"],
#         gang=groups["gang"],
#         max_hp=int(groups["max_hp"]),
#         damage=int(groups["damage"]),
#         armor=int(groups["armor"]),
#         strength=int(groups["strength"]),
#         accuracy=int(groups["accuracy"]),
#         charisma=int(groups["charisma"]),
#         dexterity=int(groups["dexterity"]),
#         max_energy=int(groups["max_energy"]),
#         uid=int(groups["id"]),
#         zen=int(groups["zen"]) - 1 if groups["zen"] else 0,
#     )


# @bot.bot.on_message(
#     filters.forwarded &
#     filters.regex(full_profile_regex) &
#     filters.create(lambda _, __, query: query.forward_from.id == BOT_WW_ID)
# )
# async def profile_handler(client: Client, message: Message):
#     update_date: float = message.forward_date.timestamp()
#     limit_time: int = 15
#     user_id = message.from_user.id
#     user_profile = parse_pipboy_data(message.text, update_date)

#     if user_profile:
#         if user_profile.uid == user_id:
#             if time.time() - update_date < limit_time:
#                 if db.get_user_profile({"id": user_id}):
#                     update_array = user_profile.compare_instances(db.get_user_profile({"id": user_profile.id}))
#                     db.update_user_profile({"id": user_profile.id}, user_profile)
#                     update_line=""
#                     for i in update_array:
#                         update_line+=f'{i}\n'
#                     await message.reply_text(f"Обновил твой пипбой!\n{update_line}")
#                 else:
#                     db.insert_profile(user_profile)
#                     await message.reply_text("Записал твой пипбой, добро пожаловать!")
#             else:
#                 await message.reply_text("Ускорься пожалуйста, ты пересылаешь его слишком медленно")
#         else:
#             await message.reply_text("Это не твой пипбой, я его не буду принимать!")
