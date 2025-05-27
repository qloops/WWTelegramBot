from .models import (
    User,
    UserSettings
)

from .base_repository import BaseRepository

from .repositories import (
    UserRepository
)

from .database import MongoDBInterface, db_interface

__all__ = [
    # Models
    "User",
    "UserSettings",

    "BaseRepository",
    
    # Repositories
    "UserRepository",
    "UserSettingsRepository",

    "MongoDBInterface",
    "db_interface",
]

def init_database(db_name: str = "WW-Telegram-Bot", host: str = "localhost", port: int = 27017) -> MongoDBInterface:
    return MongoDBInterface(db_name=db_name, host=host, port=port)