from pyrogram import Client, filters
from pyrogram.types import Message

import bot


@bot.bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id,
        text="Салам!"
    )
