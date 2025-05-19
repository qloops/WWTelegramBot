import database
import constants


def access_check(
        user: database.models.User, 
        role: constants.UserAccessRoles
) -> bool:
    """
    Checks if the user has access based on their role.

    `GOD > ADMINISTRATOR > CHAPTER > USER`

    Args:
        user: The user to check access for.
        role: The required access role.

    Returns:
        bool: True if the user has enough access, False otherwise.
    """
    return user.access_level >= role.value