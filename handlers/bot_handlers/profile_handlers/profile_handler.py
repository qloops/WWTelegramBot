from datetime import datetime, timedelta, timezone

from pyrogram import Client, filters
from pyrogram.types import Message

import bot
import database
import rules
import constants
import utils

PROFILE_UPDATE_TIMELIMIT_SECONDS = 15


def parse_profile_data(text: str, updated_at: datetime) -> database.models.FullUserProfile:
    """
    Parse profile data from message text.
    
    Args:
        text: Message text containing profile
        updated_at: Profile update timestamp
        
    Returns:
        FullUserProfile object or None if parsing failed
    """
    match = constants.patterns.ProfilePatterns.FULL_PROFILE.search(text)
 
    groups = match.groupdict()

    return database.models.FullUserProfile(
        user_id=int(groups["user_id"]),
        nickname=groups["nickname"],
        emoji_fraction=groups["emoji_fraction"],
        fraction_name=groups["fraction_name"],
        gang=groups["gang"],
        hp=int(groups["hp"]),
        damage=int(groups["damage"]),
        armor=int(groups["armor"]),
        strength=int(groups["strength"]),
        accuracy=int(groups["accuracy"]),
        charisma=int(groups["charisma"]),
        dexterity=int(groups["dexterity"]),
        energy=int(groups["energy"]),
        lid=int(groups["lid"]),
        materials=int(groups["materials"]),
        pups=int(groups["pups"]),
        zen=int(groups["zen"]) - 1 if groups["zen"] else 0,
        updated_at=updated_at
    )


@bot.bot.on_message(
    rules.filters.game_bot_forwarded &
    filters.regex(constants.patterns.ProfilePatterns.FULL_PROFILE)
)
async def profile_handler(client: Client, message: Message):
    user_id = message.from_user.id
    updated_at = utils.convert_to_utc(message.forward_date)

    user_profile = parse_profile_data(
        text=message.text, 
        updated_at=updated_at
    )

    if user_profile.user_id != user_id:
        await message.reply("Пипбой не твой, я не стану его принимать!")
        return

    if datetime.now(timezone.utc) - updated_at > timedelta(seconds=PROFILE_UPDATE_TIMELIMIT_SECONDS):
        await message.reply("Профиль устарел.")
        return

    if database.db_interface.users_profiles.exists(condition={"user_id": user_id}):
        database.db_interface.users_profiles.update_one(
            condition={"user_id": user_id}, 
            record=user_profile
        )
    else:
        database.db_interface.users_profiles.insert_one(record=user_profile)
    
    await message.reply("Обновил твой пипбой!")