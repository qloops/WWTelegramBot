from .implementations import (
    GameBotForwarded,
    UserBanned,
    EmptyProfle,
    UserAdmin
)

__all__ = [
    "game_bot_forwarded", 
    "user_banned",
    "empty_profle",
    "is_user_admin"

]

game_bot_forwarded = GameBotForwarded()
user_banned = UserBanned()
empty_profle = EmptyProfle()
is_user_admin = UserAdmin()