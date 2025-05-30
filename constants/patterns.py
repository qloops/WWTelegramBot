import re

class ProfilePatterns:
    FULL_PROFILE = re.compile(
        r"^📟Пип-бой\s3000\sv\d+\.\d+\n(Игровое\sсобытие\n\".+?\")?\n(?P<nickname>.+)"
        r",\s(?P<emoji_fraction>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction_name>.+)\n🤟Банда:\s(?P<gang>.+)"
        r"\n❤️Здоровье:\s\d+/(?P<hp>\d+)\n☠️Голод:\s\d+%\s/myfood\n⚔️Урон:\s(?P<damage>\d+)"
        r"\s🛡Броня:\s(?P<armor>\d+)(\s\(\+\d+\))?\n{2}💪Сила:\s(?P<strength>\d+)"
        r"\s🎯Меткость:\s(?P<accuracy>\d+)\n🗣Харизма:\s(?P<charisma>\d+)\s🤸🏽‍♂️Ловкость:\s(?P<dexterity>\d+)"
        r"\n💡Умения\s/perks\n⭐️Испытания\s/warpass\n{2}🔋Выносливость:\s\d+/(?P<energy>\d+)"
        r"\s/ref\n📍.+?\s👣\d+км\.\s\n{2}Экипировка:.+?Ресурсы:\n🕳Крышки:\s(?P<lid>\d+)"
        r"\s\n📦Материалы:\s(?P<materials>\d+)\n💈Пупсы:\s(?P<pups>\d+)"
        r".+?(🏵(?P<zen>\d+)\s[▓░]+\n)?ID(?P<user_id>\d+)",
        re.DOTALL
    )