from pyrogram import (
    Client,
    filters
)

from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQuery
)

import bot
import database
import keyboards
import views
import constants


# It would be nice to make a less generic handler for the profile, but I'm just 
# too lazy right now.
@bot.bot.on_inline_query(filters.create(lambda _, __, query: not query.query))
async def _(client: Client, inline_query: InlineQuery):
    user_id = inline_query.from_user.id
    text = ""

    if database.db_interface.users_profiles.exists(
        condition={"user_id": user_id}
    ):
        text = views.formatters.UserProfileFormatter.to_user_message(
            database.db_interface.users_profiles.find_one(
                condition={"user_id": user_id}
            )
        )
    else:
        text = constants.messages.COULDNT_FIND_A_PROFILE

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