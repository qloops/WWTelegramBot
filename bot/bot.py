import os

from pyrogram import Client

API_ID: str = os.environ.get("API_ID")
API_HASH: str = os.environ.get("API_HASH")
BOT_TOKEN: str = os.environ.get("BOT_TOKEN")

bot = Client(
    name="session",
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)