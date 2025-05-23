import os
import re
from datetime import datetime

from pyrogram import Client, filters
import time
import bot
from database.database import db_interface as db
from database.models import DetectedUserProfile

BOT_WW_ID = int(os.environ.get("BOT_WW_ID"))

# full_profile_regex = re.compile(
#     r"^📟Пип-бой\s3000\sv\d+\.\d+\n(Игровое\sсобытие\n\".+?\")?\n(?P<nickname>.+),\s(?P<emoji_fraction>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction>.+)\n🤟Банда:\s(?P<gang>.+)\n❤️Здоровье:\s\d+/(?P<max_hp>\d+)\n☠️Голод:\s\d+%\s/myfood\n⚔️Урон:\s(?P<damage>\d+)\s🛡Броня:\s(?P<armor>\d+)(\s\(\+\d+\))?\n{2}💪Сила:\s(?P<strength>\d+)\s🎯Меткость:\s(?P<accuracy>\d+)\n🗣Харизма:\s(?P<charisma>\d+)\s🤸🏽‍♂️Ловкость:\s(?P<dexterity>\d+)\n💡Умения\s/perks\n⭐️Испытания\s/warpass\n{2}🔋Выносливость:\s\d+/(?P<max_energy>\d+)\s/ref\n📍.+?, 👣\d+км\.\s\n{2}Экипировка:.+?(🏵(?P<zen>\d+)\s[▓░]+\n)?ID(?P<uid>\d+)",
#     re.S)
full_profile_regex = re.compile(
    r"^(?P<zone>[🚷👣])(?P<kilometr>\d+)\sкм\.\nТы\sогляделся\sвокруг\sсебя\.\s\nРядом\sкто-то\sесть\.\n\n(.+\n)*",
    re.S)



def parse_view_data(text:str, view_date:datetime):
    detected_persons = re.findall(r'(?P<name>.*) \| 👤(?P<code>.*); \n', text)
    match = full_profile_regex.search(text)
    if not match:
        return None
    groups = match.groupdict()
    line=f'{groups["zone"]}{groups["kilometr"]} ⏳{view_date.strftime("%H:%M:%S %d/%m")}\n'
    found_mimics = re.search(r'(❔Неизвестный ×(?P<mimics_count>\d*))', text).groupdict()['mimics_count']
    mimics = int(found_mimics if found_mimics else 0)
    found_not_mimics = re.search(r"(\.\.\.И еще (?P<not_mimics>\d*) выживших\.)", text).groupdict()['not_mimics']
    not_mimics = int(found_not_mimics if found_not_mimics else 0)
    all_count = mimics + not_mimics + len(detected_persons)
    line += f"Ситуация на точке:\n➖💉{mimics}/{all_count}\n🔪Подрезать:\n"
    for l in detected_persons:
        # дописать проверку на наличие ника в козле
        line += f"➖<a href='https://t.me/WastelandWarsBot?text=/p_{l[1][3:]}'>{l[0]}</a>\n"
    return line



@bot.bot.on_message(
    filters.forwarded &
    filters.regex(full_profile_regex) &
    filters.create(lambda _, __, query: query.forward_from.id == BOT_WW_ID)
)
async def my_handler(client, message):
    await message.reply_text(parse_view_data(message.text, datetime.now()), disable_web_page_preview=True)
    await message.delete()
