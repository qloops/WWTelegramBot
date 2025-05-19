from pathlib import Path
from typing import (
    Optional, 
    Any
)
from enum import Enum
import logging

from pyrogram.types import Message

import database
import bot

logger = logging.getLogger(__name__)

RESOURCES_DIR = Path(__file__).parent.parent / "resources"


class MediaCacheType(Enum):
    PHOTO = "photo"


MEDIA_CONFIG = {
    MediaCacheType.PHOTO: {
        "folder": "images",
        "send_method": "send_photo",
        "file_attr": "photo"
    }
}


async def send_cached_media(
    chat_id: int,
    file_name: str,
    media_type: MediaCacheType,
    **kwargs: Any
) -> Optional[Message]:
    try:
        config = MEDIA_CONFIG.get(media_type)

        cache_key = f"{media_type.value}:{file_name}"
        cached_file = database.db_interface.media_cache.find_one(
            condition={"cache_key": cache_key}
        )

        if cached_file:
            return await bot.bot.send_cached_media(
                chat_id=chat_id,
                file_id=cached_file.file_id,
                **kwargs
            )
        
        media_dir = RESOURCES_DIR / config["folder"]
        file_path = media_dir / file_name

        send_method = getattr(bot.bot, config["send_method"])

        media_param = media_type.value
        result = await send_method(
            chat_id=chat_id,
            **{media_param: file_path},
            **kwargs
        )

        file_attr = getattr(result, config["file_attr"], None)
        file_id = file_attr.file_id
                
        database.db_interface.media_cache.insert_one(
            database.models.MediaCache(
                cache_key=cache_key,
                file_id=file_id
            )
        )

        return result
        
    except Exception as e:
        logger.error(
            f"Error sending cached {media_type.value} {file_name}: {e}"
        )
        return None


async def send_cached_photo(
        chat_id: int, 
        file_name: str, 
        caption: str = "", 
        **kwargs
) -> Optional[Message]:
    return await send_cached_media(
        chat_id=chat_id, 
        file_name=file_name, 
        media_type=MediaCacheType.PHOTO,
        caption=caption,
        **kwargs
    )