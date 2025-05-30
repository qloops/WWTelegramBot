# database/models.py
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class User:
    """
    Represents a user in the system.
    
    Attributes:
        user_id: Telegram user ID
        administrator: Whether the user has admin privileges
        chapter: Whether the user is a chapter member
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
    """
    user_id: int
    administrator: bool = False
    chapter: bool = False
    
    created_at: datetime = field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=datetime.now(timezone.utc))


@dataclass
class UserSettings:
    """
    User-specific settings.
    
    Attributes:
        user_id: Telegram user ID
        time_zone: User's timezone offset
        pin_notification: Does the user receive raid notifications
    """
    user_id: int
    time_zone: str = "+00:00"
    pin_notification: bool = False


@dataclass
class FullUserProfile:
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