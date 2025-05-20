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

    def to_str(self):
        return (
            f"{self.nickname} {self.fraction}\n"
            f"🤟{self.gang}\n\n"
            f"🎓{self.max_hp+self.strength+self.accuracy+self.charisma+self.dexterity} "
            f"🏵{self.zen}\n"
            f"❤️{self.max_hp} ⚔️{self.damage} 🛡{self.armor}\n"
            f"💪{self.strength} 🗣{self.charisma} 🤸🏽‍♂️{self.dexterity}\n"
            f"🎯{self.accuracy} 🔋{self.max_energy}\n"
            f"UID:{self.uid}"
        )
