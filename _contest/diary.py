import re
from datetime import (
    timedelta,
    datetime,
    timezone
)

from pyrogram import (
    Client, 
    filters
)
from pyrogram.types import Message

import bot
import database
import utils
import rules

diary_regex = re.compile(
    r"^📟v\d+\.\d+\s🆔(?P<user_id>\d+)\n"
    r"ДНЕВНИК\sВЫЖИВАНИЯ\n{2}"
    r"👣Пройдено\s(?P<distance_walked_km>\d+)км;\n{2}"
    r"⚔️Убито\s(?P<mobs_killed>\d+)\sмобов;\n{2}"
    r"🔪Побеждено\s(?P<players_defeated>\d+)\sигроков;\n{2}"
    r"👁Ударил\sгиганта\s(?P<giant_hits>\d+)\sраз;\n{2}"
    r"⚜️Побеждено\s(?P<bosses_defeated>\d+)\sбоссов;\n{2}"
    r"😰Сбежал\sот\s(?P<escaped_from_enemies>\d+)\sврагов;\n{2}"
    r"👊Участвовал\sв\s(?P<raids_participated>\d+)\sрейдах;\n{2}"
    r"💉Использовано\s(?P<stimulators_used>\d+)\sстимуляторов;\n{2}"
    r"💊Использовано\s(?P<speeds_used>\d+)\sSpeed-ов;\n{2}"
    r"🚫Сломано\s(?P<items_broken>\d+)\sвещей;\n{2}"
    r"🕵️Выполнено\s(?P<quests_completed>\d+)\sпоручений;\n{2}"
    r"🎁Открыто\s(?P<gifts_opened>\d+)\sподарков;\n{2}"
    r"🎁Отправлено\s(?P<gifts_sent>\d+)\sподарков;\n{2}"
    r"🗳Открыто\s(?P<randboxes_opened>\d+)\sрандбоксов;\n{2}"
    r"💉Использовано\s(?P<steroids_used>\d+)\sстероидов\/мельдония;\n{2}"
    r"📯Пройдено\s(?P<dungeons_completed>\d+)\sподземелий;\n{2}"
    r"⚠️Прошел\sпещеру\s(?P<caves_passed>\d+)\sраз;\n{2}"
    r"⚠️Не\sпрошел\sпещеру\s(?P<caves_failed>\d+)\sраз;\n{2}"
    r"⚡️Под\sкуполом\s(?P<dome_wins>\d+)\sпобед;\n{2}"
    r"📢Пригласил\s(?P<friends_invited>\d+)\sдрузей;\n{2}"
    r"🗄Разобрал\s(?P<boxes_dismantled>\d+)\sящиков;\n{2}"
    r"⚰️Умер\s(?P<deaths>\d+)\sраз;$",
    re.DOTALL
    )

@bot.bot.on_message(filters.regex(diary_regex) & rules.game_bot_forwarded)
async def _(client: Client, message: Message):
    user_id = message.from_user.id
    if database.db_interface.users_diary.exists(
        condition={"user_id": user_id}
    ):
        await message.reply(text="Ты уже отправлял 📙Дневник, больше не нужно.")
        return
    
    diary_time = utils.convert_to_utc(message.forward_date)
    if datetime.now(timezone.utc) - diary_time > timedelta(minutes=5):
        await message.reply(text="Пришли 📙Дневник не старше 5 минут!")
        return

    match_groups = message.matches[0].groupdict()
    for key, value in match_groups.items():
        match_groups[key] = int(value)

    diary = database.models.UserDiary(
            **match_groups,
            updated_at=diary_time
        )

    if diary.user_id != user_id:
        await message.reply(
            text="📙Дневник не твой, я не стану его принимать!"
        )
        return

    database.db_interface.users_diary.insert_one(diary)
    await message.reply(text="Сохранил твой 📙Дневник.\n🍀 Удачи в конкурсе!")