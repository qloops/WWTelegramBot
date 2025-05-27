from .base_repository import BaseRepository
from .models import User, UserSettings, FullUserProfile


class UserRepository(BaseRepository[User]):
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, "users", User)


class UserSettingsRepository(BaseRepository[UserSettings]):
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, "users_settings", UserSettings)
 

class UserProfileRepository(BaseRepository[FullUserProfile]):
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, "users_profiles", FullUserProfile)
 