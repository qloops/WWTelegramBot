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
    
    def sum_of_stats(self):
        return self.dexterity + self.accuracy + self.strength + self.charisma + self.max_hp

    def compare_instances(self, class_to_compare):
        differences = []

        if self.nickname != class_to_compare.nickname:
            differences.append(str('Смена имени на'+ class_to_compare.nickname))
        if self.fraction != class_to_compare.fraction:
            differences.append(str('Смена фракции на '+ class_to_compare.fraction))
        if self.gang != class_to_compare.gang:
            differences.append(str('Смена банды на ' + class_to_compare.gang))
        if self.sum_of_stats() != class_to_compare.sum_of_stats():
            differences.append(str('🎓 '+str( self.sum_of_stats() - class_to_compare.sum_of_stats())))
        if self.damage != class_to_compare.damage:
            differences.append(str('⚔️ '+str(self.damage-class_to_compare.damage)))
        if self.armor != class_to_compare.armor:
            differences.append(str('🛡 '+str(self.armor-class_to_compare.armor)))
        if self.max_hp != class_to_compare.max_hp:
            differences.append(str('❤️ '+str(self.max_hp - class_to_compare.max_hp)))
        if self.strength != class_to_compare.strength:
            differences.append(str('💪 '+str(self.strength- class_to_compare.strength)))
        if self.accuracy != class_to_compare.accuracy:
            differences.append(str('🎯 '+str( self.accuracy- class_to_compare.accuracy)))
        if self.charisma != class_to_compare.charisma:
            differences.append(str('🗣 '+str( self.charisma - class_to_compare.charisma)))
        if self.dexterity != class_to_compare.dexterity:
            differences.append(str('🤸🏽‍♂️ '+str(self.dexterity- class_to_compare.dexterity)))
        if self.max_energy != class_to_compare.max_energy:
            differences.append(str('🔋 '+str( self.max_energy-class_to_compare.max_energy)))
        if self.zen != class_to_compare.zen:
            differences.append(str('🏵 '+str( self.uid-class_to_compare.uid)))
            differences.append('🥂Грац с дзеном!!!')
        
        return differences


@dataclass
class User:
    id: int
    settings: Dict[str, int] = field(default_factory=lambda:{"time_zone": 0, "pin_reminder": False, "raid_notify_sec": -1})
    chapter: bool = False
    administrator: bool = False