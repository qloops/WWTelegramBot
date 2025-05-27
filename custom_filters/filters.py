import os

from pyrogram import filters

BOT_WW_ID = int(os.environ.get("BOT_WW_ID"))


def game_bot_forwarded():
    def flt(_, __, query):
        if query.forward_from and query.forward_from.id == BOT_WW_ID:
            return True
        return False
    return filters.create(flt)