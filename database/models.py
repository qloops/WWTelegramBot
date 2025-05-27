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


@dataclass
class FullUserProfile:
    id: int
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

    def get_formatted_profile(self):
        return (
            f"{self.nickname} {self.emoji_fraction}\n"
            f"🤟{self.gang}\n\n"
            f"🎓{self.hp+self.strength+self.accuracy+self.charisma+self.dexterity} "
            f"🏵{self.zen}\n"
            f"❤️{self.hp} ⚔️{self.damage} 🛡{self.armor}\n"
            f"💪{self.strength} 🗣{self.charisma} 🤸🏽‍♂️{self.dexterity}\n"
            f"🎯{self.accuracy} 🔋{self.energy}\n"
            f"UID:{self.id}"
        )