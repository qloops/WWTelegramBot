import os

from .builders import (
    create_forwarded_from_filter,
    create_user_banned_filter,
    create_empty_profile_filter,
    create_is_user_admin_filter
)


class GameBotForwarded:
    BOT_WW_ID = int(os.environ["BOT_WW_ID"])

    def __new__(cls):
        return create_forwarded_from_filter(cls.BOT_WW_ID)
    

class UserBanned:
    def __new__(cls):
        return create_user_banned_filter()
    

class EmptyProfle:
    def __new__(cls):
        return create_empty_profile_filter()
    

class UserAdmin:
    def __new__(cls):
        return create_is_user_admin_filter()