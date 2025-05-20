from dataclasses import dataclass


@dataclass
class FullUserProfile:
    update_time: int
    nickname: str
    fraction: str
    gang: str
    max_hp: int
    damage: int
    armor: int
    strength: int
    accuracy: int
    charisma: int
    dexterity: int
    max_energy: int
    uid: int
    zen: int = 0
