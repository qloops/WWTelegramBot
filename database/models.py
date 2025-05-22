from typing import Dict
from dataclasses import dataclass, field


@dataclass
class FullUserProfile:
    update_time: int
    id: int
    nickname: str
    emoji_fraction: str
    gang: str
    max_hp: int
    damage: int
    armor: int
    strength: int
    accuracy: int
    charisma: int
    dexterity: int
    max_energy: int
    zen: int = 0

    def get_formatted_profile(self):
        return (
            f"{self.nickname} {self.emoji_fraction}\n"
            f"🤟{self.gang}\n\n"
            f"🎓{self.max_hp+self.strength+self.accuracy+self.charisma+self.dexterity} "
            f"🏵{self.zen}\n"
            f"❤️{self.max_hp} ⚔️{self.damage} 🛡{self.armor}\n"
            f"💪{self.strength} 🗣{self.charisma} 🤸🏽‍♂️{self.dexterity}\n"
            f"🎯{self.accuracy} 🔋{self.max_energy}\n"
            f"UID:{self.uid}"
        )


@dataclass
class User:
    id: int
    settings: Dict[str, int] = field(default_factory=lambda:{"time_zone": 0, "pin_reminder": False, "raid_notify_sec": -1})
    chapter: bool = False
    administrator: bool = False