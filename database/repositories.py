from typing import Dict, Any, Tuple

from pymongo.results import UpdateResult

from .base_repository import BaseRepository
from .models import (
    User, 
    UserSettings, 
    FullUserProfile
)


class UserRepository(BaseRepository[User]):
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, "users", User)


class UserSettingsRepository(BaseRepository[UserSettings]):
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, "users_settings", UserSettings)

    def update_timezone(self, condition: Dict[str, Any], timezone_str: str) -> UpdateResult:
        return self.update_field(
            condition=condition, 
            field_name="time_zone",
            field_value=timezone_str
        )

    def toggle_boolean_setting(self, user_id: int, setting_name: str) -> Tuple[bool, bool]:
        """
        Toggle boolean setting

        Returns:
            Tuple[bool, bool]: (operation success, new value)
        """
        settings = self.find_one({"id": user_id})
        if not settings:
            return False, False
        
        current_value = getattr(settings, setting_name, False)
        new_value = not current_value
        
        result = self.update_field(
            condition={"id": user_id},
            field_name=setting_name,
            field_value=new_value
        )
        return result.modified_count > 0, new_value


class UserProfileRepository(BaseRepository[FullUserProfile]):
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, "users_profiles", FullUserProfile)
 