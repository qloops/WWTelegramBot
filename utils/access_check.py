import database
import constants


def access_check(user: database.models.User, role: constants.UserAccessRoles) -> bool:
    """
    Checks if the user has access based on their access level.

    Compares the user's access level with the required role level.

    Notice: 
        GOD > ADMINISTRATOR > CHAPTER > USER

    Args:
        user (database.models.User): The user to check access for.
        role (constants.UserAccessRoles): The required access role.

    Returns:
        bool: True if the user has enough access, False otherwise.
    """
    return user.access_level >= role.value