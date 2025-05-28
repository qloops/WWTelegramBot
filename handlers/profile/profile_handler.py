import re
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import database
import custom_filters

full_profile_regex = re.compile(
    r"^📟Пип-бой\s3000\sv\d+\.\d+\n(Игровое\sсобытие\n\".+?\")?\n(?P<nickname>.+)"
    r",\s(?P<emoji_fraction>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction_name>.+)\n🤟Банда:\s(?P<gang>.+)"
    r"\n❤️Здоровье:\s\d+/(?P<hp>\d+)\n☠️Голод:\s\d+%\s/myfood\n⚔️Урон:\s(?P<damage>\d+)"
    r"\s🛡Броня:\s(?P<armor>\d+)(\s\(\+\d+\))?\n{2}💪Сила:\s(?P<strength>\d+)"
    r"\s🎯Меткость:\s(?P<accuracy>\d+)\n🗣Харизма:\s(?P<charisma>\d+)\s🤸🏽‍♂️Ловкость:\s(?P<dexterity>\d+)"
    r"\n💡Умения\s/perks\n⭐️Испытания\s/warpass\n{2}🔋Выносливость:\s\d+/(?P<energy>\d+)"
    r"\s/ref\n📍.+?\s👣\d+км\.\s\n{2}Экипировка:.+?Ресурсы:\n🕳Крышки:\s(?P<lid>\d+)"
    r"\s\n📦Материалы:\s(?P<materials>\d+)\n💈Пупсы:\s(?P<pups>\d+).+?(🏵(?P<zen>\d+)\s[▓░]+\n)?ID(?P<id>\d+)",
    re.S
)


def parse_pipboy_data(text: str, updated_at: datetime):
    match = full_profile_regex.search(text)
    groups = match.groupdict()

    return database.models.FullUserProfile(
        id=int(groups["id"]),
        nickname=groups["nickname"],
        emoji_fraction=groups["emoji_fraction"],
        fraction_name=groups["fraction_name"],
        gang=groups["gang"],
        hp=int(groups["hp"]),
        damage=int(groups["damage"]),
        armor=int(groups["armor"]),
        strength=int(groups["strength"]),
        accuracy=int(groups["accuracy"]),
        charisma=int(groups["charisma"]),
        dexterity=int(groups["dexterity"]),
        energy=int(groups["energy"]),
        lid=int(groups["lid"]),
        materials=int(groups["materials"]),
        pups=int(groups["pups"]),
        zen=int(groups["zen"]) - 1 if groups["zen"] else 0,
        updated_at=updated_at
    )


@bot.bot.on_message(
    custom_filters.game_bot_forwarded() &
    filters.regex(full_profile_regex)
)
async def profile_handler(client: Client, message: Message):
    user_id = message.from_user.id
    updated_at: datetime = message.forward_date
    limit_time: int = 15
    user_profile = parse_pipboy_data(text=message.text, updated_at=updated_at)

    if user_profile.id != user_id:
        await message.reply("Это не твой пипбой, я не стану его принимать!")
    else:
        if datetime.now() - updated_at < timedelta(seconds=limit_time):
            if database.db_interface.users_profiles.exists(condition={"id": user_id}):
                # update_array = user_profile.compare_instances(db.get_user_profile({"id": user_profile.id}))
                # update_line=""
                # for i in update_array:
                    # update_line+=f'{i}\n'
                # await message.reply_text(f"Обновил твой пипбой!\n{update_line}")
                database.db_interface.users_profiles.update_one(condition={"id": user_id}, record=user_profile)
            else:
                database.db_interface.users_profiles.insert_one(user_profile)
            await message.reply("Обновил твой пипбой!")
        else:
            await message.reply("/")