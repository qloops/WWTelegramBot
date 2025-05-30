from datetime import datetime, timedelta

import constants
import database
import utils


class UserProfileFormatter:
    @staticmethod
    def to_user_message(profile: database.models.FullUserProfile) -> str:
        """
        Format user profile for Telegram message.
        
        Args:
            profile: User profile to format
            
        Returns:
            Formatted string ready for Telegram
        """

        local_user_dt = UserProfileFormatter._convert_dt(
            user_id=profile.user_id,
            dt=profile.updated_at
        )

        return (
            f"{profile.emoji_fraction} <b>{profile.nickname}</b>\n"
            f"🤟 <b>{profile.gang}</b>\n\n"
            f"⚔️: <b>{profile.damage}</b>  🛡: <b>{profile.armor}</b>\n\n"
            f"❤️: <b>{profile.hp}</b>  💪: <b>{profile.strength}</b>\n"
            f"🗣: <b>{profile.charisma}</b>  🎯: <b>{profile.accuracy}</b>  🤸🏽‍♂️: <b>{profile.dexterity}</b>\n"
            f"🔋: <b>{profile.energy}</b>\n\n"
            f"БМ: <b>{profile.stats_sum}</b>\n"
            f"🏵: <b>{profile.zen}</b>\n\n"
            f"🕐:  <code>{local_user_dt}</code>\n"
            f"🆔:  <code>{profile.user_id}</code>"
        )
    
    @staticmethod
    def _convert_dt(user_id: int, dt: datetime) -> datetime:
        user_settings = database.db_interface.users_settings.find_one(condition={"user_id": user_id})
        user_tz: timedelta = constants.TIMEZONES[user_settings.time_zone]

        return utils.convert_to_timezone(
            dt=dt, 
            offset_delta=user_tz
        )