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
        return f"{self.nickname} {self.fraction}\n🤟{self.gang}\n\n🎓{self.max_hp+self.strength+self.accuracy+self.charisma+self.dexterity} 🏵{self.zen}\n❤️{self.max_hp} ⚔️{self.damage} 🛡{self.armor}\n💪{self.strength} 🗣{self.charisma} 🤸🏽‍♂️{self.dexterity}\n🎯{self.accuracy} 🔋{self.max_energy}\nUID:{self.uid}"
