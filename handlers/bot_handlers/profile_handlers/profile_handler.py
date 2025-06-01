from typing import Dict
from datetime import datetime, timedelta, timezone

from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import database
import rules
import constants
import utils

FULL_PROFILE_UPDATE_TIMELIMIT_SECONDS = 15
SHORT_PROFILE_UPDATE_TIMELIMIT_SECONDS = 5


def _construct_user_profile(
    match_groups: Dict[str, str], 
    updated_at: datetime, 
    user_id: int,
    convert_zen: bool
) -> database.models.UserProfile:
    """
    Convert extracted profile data into a UserProfile object

    Args:
        match_groups (Dict[str, str]): Dictionary containing profile data extracted using regex
        updated_at (datetime): Timestamp indicating when the profile was last updated
        user_id (int): User ID; if zero or falsy, it will be replaced with match_groups["user_id"]
        convert_zen: The flag indicates whether to subtract one from Zen

    Returns:
        UserProfile: A fully populated UserProfile instance
    """
    user_id = user_id if user_id else int(match_groups["user_id"])
    zen = int(match_groups["zen"]) if match_groups["zen"] else 0

    if convert_zen:
        zen -= 1
   
    return database.models.UserProfile(
        user_id=user_id,
        nickname=match_groups["nickname"],
        emoji_fraction=match_groups["emoji_fraction"],
        fraction_name=match_groups["fraction_name"],
        gang=match_groups["gang"],
        hp=int(match_groups["hp"]),
        damage=int(match_groups["damage"]),
        armor=int(match_groups["armor"]),
        strength=int(match_groups["strength"]),
        accuracy=int(match_groups["accuracy"]),
        charisma=int(match_groups["charisma"]),
        dexterity=int(match_groups["dexterity"]),
        energy=int(match_groups["energy"]),
        lid=int(match_groups["lid"]),
        materials=int(match_groups["materials"]),
        pups=int(match_groups["pups"]),
        zen=zen,
        updated_at=updated_at
    )


@bot.bot.on_message(
    rules.filters.game_bot_forwarded &
    filters.regex(constants.patterns.ProfilePatterns.FULL_PROFILE)
)
async def full_profile_handler(client: Client, message: Message):
    user_id = message.from_user.id
    updated_at = utils.convert_to_utc(message.forward_date)
    match_groups = message.matches[0].groupdict()
    parse_profile = _construct_user_profile(
        match_groups=match_groups, 
        updated_at=updated_at,
        user_id=user_id,
        convert_zen=True
    )

    if parse_profile.user_id != user_id:
        await message.reply("Пипбой не твой, я не стану его принимать!")
        return

    if datetime.now(timezone.utc) - updated_at > timedelta(seconds=FULL_PROFILE_UPDATE_TIMELIMIT_SECONDS):
        await message.reply("Профиль устарел.")
        return

    if database.db_interface.users_profiles.exists(condition={"user_id": user_id}):
        database.db_interface.users_profiles.update_one(
            condition={"user_id": user_id}, 
            record=parse_profile
        )
    else:
        database.db_interface.users_profiles.insert_one(record=parse_profile)
    
    await message.reply("Обновил твой пипбой!")


@bot.bot.on_message(
    rules.filters.game_bot_forwarded &
    filters.regex(constants.patterns.ProfilePatterns.SHORT_PROFILE)
)
async def short_profile_handler(client: Client, message: Message):
    user_id = message.from_user.id
    updated_at = utils.convert_to_utc(message.forward_date)
    match_groups = message.matches[0].groupdict()

    parsed_profile = _construct_user_profile(
        match_groups=match_groups, 
        updated_at=updated_at,
        user_id=user_id,
        convert_zen=True
    )

    if not database.db_interface.users_profiles.exists(condition={"user_id": user_id}):
        await message.reply("В первый раз нужен полный профиль.")
        return

    user_profile = database.db_interface.users_profiles.find_one(condition={"user_id": user_id})

    if parsed_profile.nickname != user_profile.nickname:
        await message.reply("Пипбой не твой, я не стану его принимать!")
        return

    if datetime.now(timezone.utc) - updated_at > timedelta(seconds=SHORT_PROFILE_UPDATE_TIMELIMIT_SECONDS):
        await message.reply("Профиль устарел.")
        return

    if database.db_interface.users_profiles.exists(condition={"user_id": user_id}):
        database.db_interface.users_profiles.update_one(
            condition={"user_id": user_id}, 
            record=parsed_profile
        )
    else:
        database.db_interface.users_profiles.insert_one(record=parsed_profile)
    
    await message.reply("Обновил твой пипбой!")