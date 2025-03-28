class AuthService(object):
    """
    Represents an authentication service.
    Supports login, register.
    """

    def __init__(self, users: list[str] | None = None):
        self.__users: list[str] = users or []

    def register_user(self, name: str) -> str:
        if name in self.__users:
            raise Exception('User already exists')

        self.__users.append(name)
        return name

    def login(self, name: str) -> str:
        if name not in self.__users:
            raise Exception('Invalid credentials')
        return name

