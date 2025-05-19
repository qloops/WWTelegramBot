from typing import (
    List,
    Dict
)
from dataclasses import (
    dataclass, 
    field
)
from datetime import (
    datetime, 
    timezone
)

import constants


@dataclass
class User:
    """
    Represents a user in the system.

    Attributes:
        user_id: Telegram user ID.
        access_level: The user's access level. This is the value of the 
            UserAccessRoles enum, not the enum object itself. This approach is 
            used for compatibility with MongoDB, which does not support storing 
            enum types directly.
        banned: Is this user banned?
        created_at: Timestamp when the user was created (UTC).
        updated_at: Timestamp when the user was last updated (UTC).
    """
    user_id: int
    access_level: constants.UserAccessRoles = (
        constants.UserAccessRoles.USER.value
    )
    banned: bool = False

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class UserSettings:
    """
    User-specific settings.
    
    Attributes:
        user_id: Telegram user ID.
        time_zone: User's timezone offset in format `+HH:MM` or `-HH:MM`.
        pin_notification: Does the user receive raid notifications.
    """
    user_id: int
    time_zone: str = "+00:00"
    pin_notification: bool = False


@dataclass
class UserProfile:
    user_id: int
    nickname: str
    fraction_emoji: str
    fraction_name: str
    gang_name: str
    max_hp: int
    damage: int
    armor: int
    strength: int
    accuracy: int
    charisma: int
    dexterity: int
    max_energy: int
    lids: int
    materials: int
    pups: int
    zen: int
    updated_at: datetime

    @property
    def stats_sum(self) -> int:
        return (
            self.max_hp + 
            self.strength + 
            self.accuracy + 
            self.charisma + 
            self.dexterity
        )


@dataclass
class MediaCache:
    """
    Cache for Telegram media file ID.
    
    Attributes:
        cache_key: Unique key for the cached item.
        file_id: Telegram file identifier (file_id).
    """
    cache_key: str
    file_id: str


@dataclass
class UsersGroup:
    """
    Represents a group of users.

    Attributes:
        group_name: The unique name of the group.
        group_users: A list of `user_id` objects in the group.
    """
    group_name: str
    group_users: List[int] = field(
        default_factory=lambda: []
    )


# This _contest content. 
@dataclass
class UserDiary:
    user_id: int
    distance_walked_km: int
    mobs_killed: int
    players_defeated: int
    giant_hits: int
    bosses_defeated: int
    escaped_from_enemies: int
    raids_participated: int
    stimulators_used: int
    speeds_used: int
    items_broken: int
    quests_completed: int
    gifts_opened: int
    gifts_sent: int
    randboxes_opened: int
    steroids_used: int
    dungeons_completed: int
    caves_passed: int
    caves_failed: int
    dome_wins: int
    friends_invited: int
    boxes_dismantled: int
    deaths: int

    pvp: dict = field(default_factory=dict)

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )