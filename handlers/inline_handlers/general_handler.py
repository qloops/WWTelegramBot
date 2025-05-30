from pyrogram import Client

from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQuery
)

import bot
import database
import keyboards
import views


@bot.bot.on_inline_query()
async def _(client: Client, inline_query: InlineQuery):
    user_id = inline_query.from_user.id
    user_profile = ""
    
    if database.db_interface.users_profiles.exists(condition={"user_id": user_id}):
        text = views.formatters.UserProfileFormatter.to_user_message(
            database.db_interface.users_profiles.find_one(condition={"user_id": inline_query.from_user.id})
        )
    else:
        text = "Не удалось найти профиль."

    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title=keyboards.markup_buttons.PROFILE_BUTTON,
                input_message_content=InputTextMessageContent(
                    message_text=text
                ),
                description="Отправить профиль в выбранный чат."
            )
        ],
        cache_time=0
    )