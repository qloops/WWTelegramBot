import re


class ProfilePatterns:
    FULL_PROFILE = re.compile(
        r"^📟Пип-бой\s3000\sv\d+\.\d+\n"
        r"(Игровое\sсобытие\n\".+?\")?\n(?P<nickname>.+),\s(?P<fraction_emoji>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction_name>.+)\n"
        r"🤟Банда:\s(?P<gang_name>.+)\n"
        r"❤️Здоровье:\s\d+/(?P<max_hp>\d+)\n"
        r"☠️Голод:\s\d+%\s/myfood\n"
        r"⚔️Урон:\s(?P<damage>\d+)\s🛡Броня:\s(?P<armor>\d+)(\s\(\+\d+\))?\n{2}"
        r"💪Сила:\s(?P<strength>\d+)\s🎯Меткость:\s(?P<accuracy>\d+)\n"
        r"🗣Харизма:\s(?P<charisma>\d+)\s🤸🏽‍♂️Ловкость:\s(?P<dexterity>\d+)\n"
        r"💡Умения\s/perks\n"
        r"⭐️Испытания\s/warpass\n{2}"
        r"🔋Выносливость:\s\d+/(?P<max_energy>\d+)\s/ref\n"
        r"📍.+?\s👣\d+км\.\s\n{2}"
        r"Экипировка:.+?"
        r"Ресурсы:\n"
        r"🕳Крышки:\s(?P<lids>\d+)\s\n"
        r"📦Материалы:\s(?P<materials>\d+)\n"
        r"💈Пупсы:\s(?P<pups>\d+).+?"
        r"(🏵(?P<zen>\d+)\s[▓░]+\n)?"
        r"ID(?P<user_id>\d+)",
        re.DOTALL
    )
    SHORT_PROFILE = re.compile(
        r"^👤(?P<nickname>.+?)(🏵(?P<zen>\d+))?\n"
        r"├🤟\s(?P<gang_name>.+?)\n"
        r"├(?P<fraction_emoji>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction_name>.+?)\n"
        r"├❤️\d+/(?P<max_hp>\d+)\s\|\s🍗\d+%\s\|\s⚔️(?P<damage>\d+)\s\|\s🛡(?P<armor>\d+)\n"
        r"├💪(?P<strength>\d+)\s\|\s🎯(?P<accuracy>\d+)\n"
        r"├🗣(?P<charisma>\d+)\s\|\s🤸🏽‍♂️(?P<dexterity>\d+)\n"
        r"├🔋\d+/(?P<max_energy>\d+)\s\|\s👣\d+\n"
        r".+?"
        r"├🕳(?P<lids>\d+)\n"
        r"├📦(?P<materials>\d+)💈(?P<pups>\d+)",
        re.DOTALL
    )