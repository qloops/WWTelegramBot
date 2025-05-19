from typing import Dict
from datetime import (
    datetime, 
    timedelta, 
    timezone
)
from pyrogram import (
    Client, 
    filters
)
from pyrogram.types import Message
from pyrogram.enums import ChatType

import bot
import database
import rules
import constants
import utils
import keyboards

PROFILE_UPDATE_TIMELIMITS = {
    "full": 30,
    "short": 7
}


def _construct_user_profile(
    match_groups: Dict[str, str],
    updated_at: datetime,
    user_id: int,
    convert_zen: bool
) -> database.models.UserProfile:
    """
    Convert the extracted profile data to a UserProfile object.

    Arguments:
        match_groups: dictionary containing profile data extracted using regular
            expressions.
        updated_at: timestamp indicating when the profile was last updated.
        user_id: Telegram user ID; if zero or false, it will be replaced by 
            match_groups["user_id"].
        convert_zen: flag indicating whether to subtract one from zen.

    Returns:
        UserProfile: fully populated UserProfile instance.
    """
    user_id = user_id or int(match_groups["user_id"])
    gang_name = match_groups["gang_name"].replace("Нет", "—")
    zen = int(match_groups["zen"]) if match_groups["zen"] else 0

    if convert_zen and match_groups["zen"]:
        zen -= 1
   
    return database.models.UserProfile(
        user_id=user_id,
        nickname=match_groups["nickname"],
        fraction_emoji=match_groups["fraction_emoji"],
        fraction_name=match_groups["fraction_name"],
        gang_name=gang_name,
        max_hp=int(match_groups["max_hp"]),
        damage=int(match_groups["damage"]),
        armor=int(match_groups["armor"]),
        strength=int(match_groups["strength"]),
        accuracy=int(match_groups["accuracy"]),
        charisma=int(match_groups["charisma"]),
        dexterity=int(match_groups["dexterity"]),
        max_energy=int(match_groups["max_energy"]),
        lids=int(match_groups["lids"]),
        materials=int(match_groups["materials"]),
        pups=int(match_groups["pups"]),
        zen=zen,
        updated_at=updated_at
    )


async def _validate_profile(
    message: Message,
    parsed_profile: database.models.UserProfile,
    profile_type: str
) -> bool:
    updated_at = utils.convert_to_utc(message.forward_date)
    time_limit = timedelta(seconds=PROFILE_UPDATE_TIMELIMITS[profile_type])
    user_id = message.from_user.id
    
    if datetime.now(timezone.utc) - updated_at > time_limit:
        await message.reply(text="Профиль устарел.")
        return False

    if profile_type == "full":
        if parsed_profile.user_id != user_id:
            await message.reply(
                text="Профиль не твой, я не стану его принимать!"
            )
            return False
    else:  # Short profile.
        if not database.db_interface.users_profiles.exists(
            condition={"user_id": user_id}
        ):
            await message.reply(text="В первый раз нужен полный профиль.")
            return False

        user_profile = database.db_interface.users_profiles.find_one(
            condition={"user_id": user_id}
        )
        
        if parsed_profile.nickname != user_profile.nickname:
            await message.reply(
                text="Профиль не твой, я не стану его принимать!"
            )
            return False
    
    return True


async def _save_profile(
    user_id: int, 
    profile: database.models.UserProfile
):
    condition = {"user_id": user_id}
    
    if database.db_interface.users_profiles.exists(condition=condition):
        database.db_interface.users_profiles.update_one(
            condition=condition,
            record=profile
        )
    else:
        database.db_interface.users_profiles.insert_one(record=profile)


async def _handle_profile(
    message: Message,
    profile_type: str
):
    user_id = 0 if profile_type == "full" else message.from_user.id
    updated_at = utils.convert_to_utc(message.forward_date)
    match_groups = message.matches[0].groupdict()
    
    # Only convert zen for full profiles.
    convert_zen = (profile_type == "full")

    parsed_profile = _construct_user_profile(
        match_groups=match_groups,
        updated_at=updated_at,
        user_id=user_id,
        convert_zen=convert_zen
    )
    
    if not await _validate_profile(
        message, 
        parsed_profile, 
        profile_type
    ):
        return
    
    await _save_profile(parsed_profile.user_id, parsed_profile)
    
    if profile_type == "full":
        database.utils.create_new_user.create_new_user(parsed_profile.user_id)
    
    if message.chat.type == ChatType.PRIVATE:
        await message.reply(
            text="Обновил твой профиль!", 
            reply_markup=keyboards.markup_keyboards.MENU_KEYBOARD
        )
    else:
        await message.reply(text="Обновил твой профиль!")


@bot.bot.on_message(
    rules.game_bot_forwarded &
    filters.regex(constants.patterns.ProfilePatterns.FULL_PROFILE)
)
async def full_profile_handler(client: Client, message: Message):
    await _handle_profile(message, "full")


@bot.bot.on_message(
    rules.game_bot_forwarded &
    filters.regex(constants.patterns.ProfilePatterns.SHORT_PROFILE)
)
async def short_profile_handler(client: Client, message: Message):
    await _handle_profile(message, "short")