from dataclasses import dataclass, field
from datetime import datetime, timezone

import constants


@dataclass
class User:
    """
    Represents a user in the system.

    Attributes:
        user_id (int): Telegram user ID
        access_level (str): The user's access level. This is the value of the UserAccessRoles enum,
            not the enum object itself. This approach is used for compatibility with MongoDB, 
            which does not support storing enum types directly
        banned (bool): Is this user banned?
        created_at (datetime): Timestamp when the user was created (UTC)
        updated_at (datetime): Timestamp when the user was last updated (UTC)
    """
    user_id: int
    access_level: constants.UserAccessRoles = constants.UserAccessRoles.USER.value
    banned: bool = False

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class UserSettings:
    """
    User-specific settings.
    
    Attributes:
        user_id: Telegram user ID
        time_zone (str): User's timezone offset in format '+HH:MM' or '-HH:MM'
        pin_notification: Does the user receive raid notifications
    """
    user_id: int
    time_zone: str = "+00:00"
    pin_notification: bool = False


@dataclass
class UserProfile:
    user_id: int
    nickname: str
    emoji_fraction: str
    fraction_name: str
    gang: str
    hp: int
    damage: int
    armor: int
    strength: int
    accuracy: int
    charisma: int
    dexterity: int
    energy: int
    lid: int
    materials: int
    pups: int
    zen: int
    updated_at: datetime

    @property
    def stats_sum(self) -> int:
        return self.hp + self.strength + self.accuracy + self.charisma + self.dexterity


@dataclass
class MediaCache:
    """
    Cache for Telegram media file ID.
    
    Attributes:
        cache_key: Unique key for the cached item
        file_id: Telegram file identifier (file_id)
    """
    cache_key: str
    file_id: str