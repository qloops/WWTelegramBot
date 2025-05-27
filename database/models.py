from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: int
    administrator: bool = False
    chapter: bool = False
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class UserSettings:
    id: int
    time_zone: float = 0.
    raid_notify_sec: float = 0.
    pin_notification: bool = False