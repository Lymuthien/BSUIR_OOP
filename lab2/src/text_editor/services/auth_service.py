from ..interfaces import IUser
from ..models import User


class AuthService(object):
    """
    Represents an authentication service.
    Supports login, register.
    """

    def __init__(self, users: dict[str: IUser] | None = None):
        self.__users: dict[str: IUser] = users or {}  # name -> user

    def register_user(self, name: str, password: str) -> IUser:
        """
        Register a new user.

        :param name: Name.
        :param password: Password.
        :return: AuthUser object.
        :raise Exception: If user already exists.
        """

        if self.__users.get(name):
            raise Exception('User already exists')

        user = User(name, password)
        self.__users[name] = user

        return user

    def login(self, name: str, password: str) -> IUser:
        """
        Login with email and password.

        :param name: Name.
        :param password: Password.
        :return: User object if login was successful.
        :raise Exception: If user not found.
        """

        user = self.__users.get(name)
        if not user or not user.validate_password(password):
            raise Exception('Invalid credentials')

        return user

