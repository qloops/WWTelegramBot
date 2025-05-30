from typing import TYPE_CHECKING, Dict, Any, Tuple

from pymongo.results import UpdateResult

from .base_repository import BaseRepository
from .models import (
    User, 
    UserSettings, 
    FullUserProfile,
    MediaCache
)

if TYPE_CHECKING:
    from .database import MongoDBInterface


class UserRepository(BaseRepository[User]):
    COLLECTION_NAME = "users"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, User)


class UserSettingsRepository(BaseRepository[UserSettings]):
    COLLECTION_NAME = "users_settings"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, UserSettings)

    def update_timezone(self, user_id: int, timezone_str: str) -> UpdateResult:
        """
        Update user timezone setting.

        Args:
            user_id: User identifier
            timezone_str: New timezone string value
            
        Returns:
            UpdateResult: MongoDB update operation result
        """
        return self.update_field(
            condition={"user_id": user_id}, 
            field_name="time_zone",
            field_value=timezone_str
        )

    def toggle_boolean_setting(self, user_id: int, setting_name: str) -> Tuple[bool, bool]:
        """
        Toggle boolean setting for a user.
        
        Args:
            user_id: User identifier
            setting_name: Name of the boolean setting to toggle
            
        Returns:
            Tuple[bool, bool]: (operation success, new value)
        """
        settings = self.find_one({"user_id": user_id})
        if not settings:
            return False, False
        
        current_value = getattr(settings, setting_name, False)
        new_value = not current_value
        
        result = self.update_field(
            condition={"user_id": user_id},
            field_name=setting_name,
            field_value=new_value
        )
        return result.modified_count > 0, new_value


class UserProfileRepository(BaseRepository[FullUserProfile]):
    COLLECTION_NAME = "users_profile"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, FullUserProfile)
 

class MediaCacheRepository(BaseRepository[MediaCache]):
    COLLECTION_NAME = "media_cache"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, MediaCache)