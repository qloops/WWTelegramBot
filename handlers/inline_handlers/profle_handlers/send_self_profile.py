from pyrogram import Client

from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQuery
)

import bot
import database
import views

@bot.bot.on_inline_query()
async def answer(client: Client, inline_query: InlineQuery):
    text = ""
    
    if database.db_interface.users_profile.exists(condition={"user_id": inline_query.from_user.id}):
        text = views.formatters.UserProfileFormatter.to_user_message(database.db_interface.users_profile.find_one(condition={"user_id": inline_query.from_user.id}))
    else: 
        text = "Не удалось найти профиль."
    
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Отправить профиль",
                input_message_content=InputTextMessageContent(
                    message_text=text
                ),
                description="Отправить профиль в выбранный чат"
            )
        ],
        cache_time=0
    )
