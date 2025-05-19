from pyrogram import Client
from pyrogram.types import InlineQuery

import bot
import rules


@bot.bot.on_inline_query(rules.user_banned)
async def banned_handler(client: Client, inline_query: InlineQuery):
    # Ignore inline requests from banned players.
    return


@bot.bot.on_inline_query(rules.empty_profle)
async def empty_profile_handler(client: Client, inline_query: InlineQuery):
    # Ignore inline requests from empty profile players.
    return