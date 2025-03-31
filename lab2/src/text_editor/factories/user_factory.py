from abc import abstractmethod, ABC

from ..models.user import IUser, EditorUser, Admin, ReaderUser


class UserFactory(ABC):
    @abstractmethod
    def create_user(self, name: str = 'base') -> IUser: ...


class EditorUserFactory(UserFactory):
    def create_user(self, name: str = 'base') -> IUser:
        return EditorUser(name)


class AdminUserFactory(UserFactory):
    def create_user(self, name: str = 'base') -> IUser:
        return Admin(name)


class ReaderUserFactory(UserFactory):
    def create_user(self, name: str = 'base') -> IUser:
        return ReaderUser(name)


users: dict[str, UserFactory] = {
    Admin.__name__.lower(): AdminUserFactory(),
    EditorUser.__name__.lower(): EditorUserFactory(),
    ReaderUser.__name__.lower(): ReaderUserFactory(),
}
