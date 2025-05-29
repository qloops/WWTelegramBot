from .models import FullUserProfile


class UserProfileFormatter:
    @staticmethod
    def to_telegram_message(profile: FullUserProfile) -> str:
        """
        Format user profile for Telegram message.
        
        Args:
            profile: User profile to format
            
        Returns:
            Formatted string ready for Telegram
        """
        return (
            f"{profile.nickname} {profile.emoji_fraction}\n"
            f"🤟{profile.gang}\n\n"
            f"🎓{profile.stats_sum} "
            f"🏵{profile.zen}\n"
            f"❤️{profile.hp} ⚔️{profile.damage} 🛡{profile.armor}\n"
            f"💪{profile.strength} 🗣{profile.charisma} 🤸🏽‍♂️{profile.dexterity}\n"
            f"🎯{profile.accuracy} 🔋{profile.energy}\n"
            f"UID:{profile.user_id}"
        )