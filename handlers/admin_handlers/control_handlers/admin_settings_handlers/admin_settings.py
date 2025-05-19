import logging
from typing import Optional

from pyrogram import (
    Client, 
    filters
)
from pyrogram.types import CallbackQuery
from pyrogram.errors import MessageNotModified

import bot
import keyboards
import database
import views
import utils
import constants

logger = logging.getLogger(__name__)


class CallbackHandlers:
    @staticmethod
    async def _validate_admin_access(
        call: CallbackQuery, 
        required_role: constants.UserAccessRoles = (
            constants.UserAccessRoles.ADMINISTRATOR
        )
    ) -> Optional[dict]:
        user = database.db_interface.users.find_one(
            condition={"user_id": call.from_user.id}
        )
        if not utils.access_check(user, required_role):
            await call.answer(constants.messages.NO_ACCESS)
            return None
        return user

    @staticmethod
    async def _get_reply_user(user_id: int) -> dict:
        return database.db_interface.users.find_one(
            condition={"user_id": user_id}
        )

    @staticmethod
    async def _update_user_view(
        call: CallbackQuery, 
        reply_user_id: int, 
        admin_id: int
    ) -> None:
        reply_user_profile = database.db_interface.users_profiles.find_one(
            condition={"user_id": reply_user_id}
        )
        reply_user = database.db_interface.users.find_one(
            condition={"user_id": reply_user_id}
        )

        try:
            await call.message.edit(
                text=views.UserProfileFormatter.to_admin_message(
                    reply_user_profile, 
                    admin_id=admin_id
                ),
                reply_markup=(
                    keyboards.builders.create_admin_settings_user_keyboard(
                        reply_user
                    )
                )  
            )
        except MessageNotModified:
            pass


@bot.bot.on_callback_query(
    filters.regex(r"^admin_change_(?P<change_name>.+?)_(?P<user_id>\d+)$")
)
async def admin_change_user_callback(client: Client, call: CallbackQuery):
    user = await CallbackHandlers._validate_admin_access(call)
    if not user:
        return

    change_name = call.matches[0].group("change_name")
    reply_user_id = int(call.matches[0].group("user_id"))
    reply_user = await CallbackHandlers._get_reply_user(reply_user_id)

    if reply_user.user_id == user.user_id:
        await call.answer(text="Нельзя себя.")
        return
    
    if reply_user.access_level >= constants.UserAccessRoles.ADMINISTRATOR.value:
        await call.answer(text=constants.messages.NO_ACCESS)
        return

    await _process_user_change(change_name, reply_user_id, reply_user)
    await CallbackHandlers._update_user_view(call, reply_user_id, user.user_id)
    await call.answer(constants.messages.SUCCESSFULLY)


async def _process_user_change(
        change_name: str, 
        reply_user_id: int, 
        reply_user: dict
) -> None:
    if change_name == "user_chapter":
        new_access_level = (
            constants.UserAccessRoles.CHAPTER.value 
            if reply_user.access_level == constants.UserAccessRoles.USER.value
            else constants.UserAccessRoles.USER.value
        )
        database.db_interface.users.update_field(
            condition={"user_id": reply_user_id}, 
            field_name="access_level", 
            field_value=new_access_level
        )
    elif change_name == "user_banned":
        database.db_interface.users.toggle_boolean_parametrs(
            user_id=reply_user_id, 
            parametr_name="banned"
        )


@bot.bot.on_callback_query(
    filters.regex(r"^remove_user_from_gang_(?P<user_id>\d+)$")
)
async def remove_user_from_gang_callback(client: Client, call: CallbackQuery):
    if not await CallbackHandlers._validate_admin_access(
        call, 
        constants.UserAccessRoles.CHAPTER
    ):
        return

    reply_user_id = int(call.matches[0].group("user_id"))
    await call.message.edit_reply_markup(
        reply_markup=keyboards.builders.confirm_deletion_keyboard(reply_user_id)
    )


@bot.bot.on_callback_query(
    filters.regex(r"^(?P<confirm_status>yes|no)_delete_(?P<user_id>\d+)$")
)
async def confirm_deletion_callback(client: Client, call: CallbackQuery):
    user = await CallbackHandlers._validate_admin_access(
        call, 
        constants.UserAccessRoles.CHAPTER
    )
    if not user:
        return

    confirm_status = call.matches[0].group("confirm_status")
    reply_user_id = int(call.matches[0].group("user_id"))
    
    if confirm_status == "yes":
        logger.info(
            f"User {user.user_id} removed player {reply_user_id} from the gang."
        )
        database.db_interface.users_profiles.update_field(
            condition={"user_id": reply_user_id}, 
            field_name="gang_name", 
            field_value="—"
        )

    await CallbackHandlers._update_user_view(call, reply_user_id, user.user_id)
    
    if confirm_status == "yes":
        await call.answer(constants.messages.SUCCESSFULLY)