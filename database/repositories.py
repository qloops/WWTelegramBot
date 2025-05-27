from .base_repository import BaseRepository
from .models import User, UserSettings


class UserRepository(BaseRepository[User]):
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, "users", User)


class UserSettingsRepository(BaseRepository[UserSettings]):
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, "users_settings", UserSettings)
 