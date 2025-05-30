from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import keyboards
import utils


@bot.bot.on_message(filters.regex(f"^{keyboards.markup_buttons.CONTROL_BUTTON}$"))
async def control_button(client: Client, message: Message):
    await utils.send_cached_image(chat_id=message.chat.id, file_name="technical_work.png", caption="🪛⚙️ Technical work")