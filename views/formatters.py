from database import models


class UserProfileFormatter:
    @staticmethod
    def to_user_message(profile: models.FullUserProfile) -> str:
        """
        Format user profile for Telegram message.
        
        Args:
            profile: User profile to format
            
        Returns:
            Formatted string ready for Telegram
        """
        return (
            f"{profile.emoji_fraction} <b>{profile.nickname}</b>\n"
            f"🤟 <b>{profile.gang}</b>\n\n"
            f"⚔️: <b>{profile.damage}</b>  🛡: <b>{profile.armor}</b>\n"
            f"🔋: <b>{profile.energy}</b>  🏵: <b>{profile.zen}</b>\n\n"
            f"❤️: <b>{profile.hp}</b>  💪: <b>{profile.strength}</b>\n"
            f"🗣: <b>{profile.charisma}</b>  🎯: <b>{profile.accuracy}</b>  🤸🏽‍♂️: <b>{profile.dexterity}</b>\n\n"
            f"БМ: <b>{profile.stats_sum}</b>\n\n"
            f"🕐:  <code>{profile.updated_at}</code>\n"
            f"🆔:  <code>{profile.user_id}</code>"
        )