from pyrogram.types import (
    Message,
    InlineQuery
)
from pyrogram import filters
from pyrogram.enums import ChatType

import database
import constants


def create_forwarded_from_filter(user_id: int):
    async def func(_, __, query: Message):
        return query.forward_from and query.forward_from.id == user_id
    
    return filters.create(func)


def create_user_banned_filter():
    async def func(_, __, query: Message | InlineQuery):
        if isinstance(query, Message) and query.chat.type == ChatType.CHANNEL:
            return True
        elif (
            isinstance(query, InlineQuery) and 
            query.chat_type == ChatType.CHANNEL
        ):
            return True
        if isinstance(query, (Message, InlineQuery)):
            user = database.db_interface.users.find_one(
                condition={"user_id": query.from_user.id}
            )
            if user:
                return user.banned
        return False

    return filters.create(func)


def create_empty_profile_filter():
    async def func(_, __, query: Message | InlineQuery):
        return not database.db_interface.users_profiles.exists(
            condition={"user_id": query.from_user.id}
        )

    return filters.create(func)


def create_is_user_admin_filter():
    async def func(_, __, query: Message | InlineQuery):
        user = database.db_interface.users.find_one(
            condition={"user_id": query.from_user.id}
        )
        if user:
            return (
                user.access_level >= 
                constants.UserAccessRoles.ADMINISTRATOR.value
            )

    return filters.create(func)