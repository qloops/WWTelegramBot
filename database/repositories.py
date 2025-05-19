import logging
from typing import (
    TYPE_CHECKING, 
    Tuple, 
    List,
    TypeVar
)

from pymongo.results import UpdateResult

from .base_repository import BaseRepository
from .models import (
    User, 
    UserSettings, 
    UserProfile,
    MediaCache,
    UsersGroup,

    # This _contest content. 
    UserDiary
)

if TYPE_CHECKING:
    from .database import MongoDBInterface

T = TypeVar("T")

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User]):
    COLLECTION_NAME = "users"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, User)
    
    def toggle_boolean_parametrs(
            self, 
            user_id: int, 
            parametr_name: str
    ) -> Tuple[bool, bool]:
        """
        Toggle boolean parametrs for a user.
        
        Args:
            user_id: Telegram user ID.
            setting_name: Name of the boolean parametr to toggle.
            
        Returns:
            Tuple[bool, bool]: (operation success, new value).
        """
        parametr = self.find_one({"user_id": user_id})
        if not parametr:
            return False, False
        
        current_value = getattr(parametr, parametr_name, False)
        new_value = not current_value

        result = self.update_field(
            condition={"user_id": user_id},
            field_name=parametr_name,
            field_value=new_value
        )
        return result.modified_count > 0, new_value


class UserSettingsRepository(BaseRepository[UserSettings]):
    COLLECTION_NAME = "users_settings"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, UserSettings)

    def update_timezone(self, user_id: int, timezone_str: str) -> UpdateResult:
        """
        Update user timezone setting.

        Args:
            user_id: Telegram user ID.
            timezone_str: New timezone string value.
            
        Returns:
            UpdateResult: MongoDB update operation result.
        """
        return self.update_field(
            condition={"user_id": user_id}, 
            field_name="time_zone",
            field_value=timezone_str
        )

    def toggle_boolean_setting(
            self, 
            user_id: int, 
            setting_name: str
    ) -> Tuple[bool, bool]:
        """
        Toggle boolean setting for a user.
        
        Args:
            user_id: Telegram user ID.
            setting_name: Name of the boolean setting to toggle.
            
        Returns:
            Tuple[bool, bool]: (operation success, new value).
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


class UserProfileRepository(BaseRepository[UserProfile]):
    COLLECTION_NAME = "users_profiles"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, UserProfile)
    
    def get_unique_gangs_names(self) -> List[str]:
        """
        Get a list of unique values for the "gang_name" field in the collection.
        
        Returns:
            List[str]: List of unique gang names.
        """
        return self._db._get_distinct_values(
            collection_name=self._collection_name, 
            field_name="gang_name"
        )


class MediaCacheRepository(BaseRepository[MediaCache]):
    COLLECTION_NAME = "media_cache"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, MediaCache)


class UsersGroupRepository(BaseRepository[UsersGroup]):
    COLLECTION_NAME = "users_groups"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, UsersGroup)


# This _contest content.
class UsersDiaryRepository(BaseRepository[UserDiary]):
    COLLECTION_NAME = "users_diary"
    
    def __init__(self, db_interface: "MongoDBInterface"):
        super().__init__(db_interface, self.COLLECTION_NAME, UserDiary)
    
    
    def add_diary_entry(
        self, 
        user_id: int, 
        field_name: str,
        key: str,
        entry_data: dict
    ) -> UpdateResult:
        """
        Add a new entry to a dictionary field in user's diary.
        
        Args:
            user_id: Telegram user ID.
            field_name: Name of the dictionary field.
            key: Key for the new entry in the dictionary.
            entry_data: Dictionary with the entry data.
            
        Returns:
            UpdateResult: MongoDB update operation result.
        """
        return self._db._update_one(
            collection_name=self._collection_name,
            condition={"user_id": user_id},
            update_operations={"$set": {f"{field_name}.{key}": entry_data}}
        )