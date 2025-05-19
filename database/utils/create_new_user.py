import database

def create_new_user(user_id: int):
    """
    Initializes all necessary database records for a new user.

    This function checks if the required records for the given `user_id` exist 
        in the database. If any are missing, it creates them. This ensures that 
        all essential user-related data structures are properly initialized.

    Args:
        user_id: Telegram user ID.
    """
    if not database.db_interface.users.exists(condition={"user_id": user_id}):
        database.db_interface.users.insert_one(
            database.models.User(user_id=user_id)
        )
    if not database.db_interface.users_settings.exists(
        condition={"user_id": user_id}
    ):
        database.db_interface.users_settings.insert_one(
            database.models.UserSettings(user_id=user_id)
        )