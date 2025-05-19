from datetime import datetime, timedelta, timezone

import constants
import database
import utils


class UserProfileFormatter:
    @staticmethod
    def to_user_message(user_profile: database.models.UserProfile) -> str:
        return UserProfileFormatter._format_profile(
            profile=user_profile,
            viewer_id=user_profile.user_id,
            show_balance=False
        )

    @staticmethod
    def to_admin_message(
        user_profile: database.models.UserProfile, 
        admin_id: int
    ) -> str:
        return UserProfileFormatter._format_profile(
            profile=user_profile,
            viewer_id=admin_id,
            show_balance=True
        )

    @staticmethod
    def _format_profile(
        profile: database.models.UserProfile, 
        viewer_id: int,
        show_balance: bool
    ) -> str:
        local_dt = UserProfileFormatter._convert_dt(
            viewer_id=viewer_id,
            dt=profile.updated_at
        )
        if show_balance:
            return (
                f"{profile.fraction_emoji} <b>{profile.nickname}</b>\n"
                f"🤟 <b>{profile.gang_name}</b>\n\n"
                f"⚔️: <b>{profile.damage}</b>  🛡: <b>{profile.armor}</b>\n\n"
                f"❤️: <b>{profile.max_hp}</b>  💪: <b>{profile.strength}</b>\n"
                f"🗣: <b>{profile.charisma}</b>  🎯: <b>{profile.accuracy}</b>"
                f"  🤸🏽‍♂️: <b>{profile.dexterity}</b>\n"
                f"🔋: <b>{profile.max_energy}</b>  💈: <b>{profile.pups}</b>\n"
                f"🕳: <b>{profile.lids}</b>  📦: <b>{profile.materials}</b>\n\n"
                f"БМ: <b>{profile.stats_sum}</b>\n"
                f"🏵: <b>{profile.zen}</b>\n\n"
                f"🕐:  <code>{local_dt}</code>\n"
                f"🆔:  <code>{profile.user_id}</code>"
            )
        else:
            return (
                f"{profile.fraction_emoji} <b>{profile.nickname}</b>\n"
                f"🤟 <b>{profile.gang_name}</b>\n\n"
                f"⚔️: <b>{profile.damage}</b>  🛡: <b>{profile.armor}</b>\n\n"
                f"❤️: <b>{profile.max_hp}</b>  💪: <b>{profile.strength}</b>\n"
                f"🗣: <b>{profile.charisma}</b>  🎯: <b>{profile.accuracy}</b>"
                f"  🤸🏽‍♂️: <b>{profile.dexterity}</b>\n"
                f"🔋: <b>{profile.max_energy}</b>\n\n"
                f"БМ: <b>{profile.stats_sum}</b>\n"
                f"🏵: <b>{profile.zen}</b>\n\n"
                f"🕐:  <code>{local_dt}</code>\n"
                f"🆔:  <code>{profile.user_id}</code>"
            )
    # TODO: This function is not intended to be called directly, but is 
    # available in some parts of other modules, which needs to be fixed.
    @staticmethod
    def _convert_dt(viewer_id: int, dt: datetime) -> datetime:
        user_settings = database.db_interface.users_settings.find_one(
            condition={"user_id": viewer_id}
        )
        local_time_tz: timedelta = constants.TIMEZONES[user_settings.time_zone]
        return utils.shift_to_timezone(
            dt=dt, 
            offset_delta=local_time_tz
        )


class UserSettingsFormatter:
    @staticmethod
    def to_notify_message(user_settings: database.models.UserSettings) -> str:
        notify_pin_status_emoji = (
            constants.messages.CHECK_MARK 
            if user_settings.pin_notification 
            else constants.messages.CROSS_MARK
        )
        return (
            "<b>🔔 Уведомления:</b>"
            f"\n\n{notify_pin_status_emoji} Рейды"
            "\n<i>(Уведомлять о пинах.)</i>"
        )
    
    @staticmethod
    def to_time_zone_setting(
        user_settings: database.models.UserSettings
    ) -> str:
        local_user_dt = UserProfileFormatter._convert_dt(
            viewer_id=user_settings.user_id, 
            dt=datetime.now(timezone.utc)
        )
    
        local_user_dt = local_user_dt.replace(microsecond=0)
        local_user_dt = local_user_dt.replace(tzinfo=None)
        return (
            f"🕐 Твоё время: <code>{local_user_dt}</code>"
            f"\nВыбранный пояс: <b>{user_settings.time_zone}</b>"
        )