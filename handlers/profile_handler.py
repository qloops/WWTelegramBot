import os
import re
from pyrogram import Client, filters
import time
import bot
from database.database import db_interface as db
from database.models import FullUserProfile

BOT_WW_ID = int(os.environ.get("BOT_WW_ID"))

full_profile_regex = re.compile(
    r"^📟Пип-бой\s3000\sv\d+\.\d+\n(Игровое\sсобытие\n\".+?\")?\n(?P<nickname>.+),\s(?P<emoji_fraction>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction>.+)\n🤟Банда:\s(?P<gang>.+)\n❤️Здоровье:\s\d+/(?P<max_hp>\d+)\n☠️Голод:\s\d+%\s/myfood\n⚔️Урон:\s(?P<damage>\d+)\s🛡Броня:\s(?P<armor>\d+)(\s\(\+\d+\))?\n{2}💪Сила:\s(?P<strength>\d+)\s🎯Меткость:\s(?P<accuracy>\d+)\n🗣Харизма:\s(?P<charisma>\d+)\s🤸🏽‍♂️Ловкость:\s(?P<dexterity>\d+)\n💡Умения\s/perks\n⭐️Испытания\s/warpass\n{2}🔋Выносливость:\s\d+/(?P<max_energy>\d+)\s/ref\n📍.+?, 👣\d+км\.\s\n{2}Экипировка:.+?(🏵(?P<zen>\d+)\s[▓░]+\n)?ID(?P<uid>\d+)",
    re.S)


def parse_pipboy_data(text: str, update1_time):
    match = full_profile_regex.search(text)
    if not match:
        return None

    groups = match.groupdict()

    return FullUserProfile(
        nickname=groups['nickname'].strip(),
        fraction=groups['emoji_fraction'].strip(),
        gang=groups['gang'].strip(),
        max_hp=int(groups['max_hp']),
        damage=int(groups['damage']),
        armor=int(groups['armor']),
        strength=int(groups['strength']),
        accuracy=int(groups['accuracy']),
        charisma=int(groups['charisma']),
        dexterity=int(groups['dexterity']),
        max_energy=int(groups['max_energy']),
        uid=int(groups['uid']),
        zen=int(groups['zen'])-1 if groups['zen'] else 0,
        update_time=update1_time
    )


@bot.bot.on_message(
    filters.forwarded &
    filters.regex(full_profile_regex) &
    filters.create(lambda _, __, query: query.forward_from.id == BOT_WW_ID)
)
async def my_handler(client, message):
    user_profile = parse_pipboy_data(message.text, message.forward_date.timestamp())
    if user_profile:
        if user_profile.uid == message.from_user.id:
            if time.time() - message.forward_date.timestamp() < 15:
                if db.get_user_profile({'uid': user_profile.uid}):
                    db.update_user_profile({'uid': user_profile.uid}, user_profile)
                    await message.reply_text("Обновил твой пипбой!")
                else:
                    db.insert_profile(user_profile)
                    await message.reply_text("Записал твой пипбой, добро пожаловать!")
            else:
                await message.reply_text("Ускорься пожалуйста, ты пересылаешь его слишком медленно")
        else:
            await message.reply_text("Это не твой пипбой, я его не буду принимать!")
