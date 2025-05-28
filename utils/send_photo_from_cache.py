from pathlib import Path

import database
import bot

current_file = Path(__file__)
image_dir_path = current_file.parent.parent / "resources" / "images"


async def send_cached_image(chat_id: int, file_name: str, **kwards):
    if database.db_interface.media_cache.exists(condition={"file_name": file_name}):
        file = database.db_interface.media_cache.find_one(condition={"file_name": file_name})
        await bot.bot.send_cached_media(chat_id=chat_id, file_id=file.file_id, **kwards)
    else:
        image_path = image_dir_path / file_name
        result = await bot.bot.send_photo(chat_id=chat_id, photo=image_path, **kwards)
        
        database.db_interface.media_cache.insert_one(
            database.models.MediaCache(file_name=file_name, file_id=result.photo.file_id)
        )