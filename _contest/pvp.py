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

opponents_regex = re.compile(
    r"(?P<name_one>.+?)\sиз\s[🔪💣🔰⚛️⚙️👙🤕].+\n"
    r"VS\.\n"
    r"(?P<name_two>.+?)\sиз\s[🔪💣🔰⚛️⚙️👙🤕].+\nFIGHT!"
    )


@bot.bot.on_message(filters.regex(opponents_regex) & rules.game_bot_forwarded)
async def _(client: Client, message: Message):
    user_id = message.from_user.id
    if not database.db_interface.users_diary.exists(
        condition={"user_id": user_id}
    ):
        await message.reply(text="Сначала нужно отправить 📙Дневник.")
        return
    
    if re.search(r"📊ТОП\sКупола\s/tdtop", message.text):
        return

    opponent_one = message.matches[0].group("name_one")
    opponent_two = message.matches[0].group("name_two")
    winner = None

    if re.search(rf".+[❤️🛰].+\n\n{opponent_one}\s.+", message.text):
        winner = opponent_one
    elif re.search(rf".+[❤️🛰].+\n\n{opponent_two}\s.+", message.text):
        winner = opponent_two

    
    diary_time = utils.convert_to_utc(message.forward_date)
    if datetime.now(timezone.utc) - diary_time > timedelta(minutes=5):
        await message.reply(text="Пришли сражение не старше 5 минут!")
        return
    
    diary_time_key = diary_time.isoformat()

    data = {
        "opponent_one": opponent_one,
        "opponent_two": opponent_two,
        "winner": winner,
        "timestamp": diary_time
    }

    if database.db_interface.users_diary.exists(
        condition={
            "user_id": user_id,
            f"pvp.{diary_time_key}": {"$exists": True}
        }
    ):
        await message.reply(text="Ты уже отправлял это сражение.")
        return

    database.db_interface.users_diary.add_diary_entry(
        user_id=user_id,
        field_name="pvp",
        key=diary_time_key,
        entry_data=data
    )
    await message.reply(text="Сохранил это сражение.")