import datetime

from .password_manager import PasswordManager
from ..interfaces import IUser


class User(IUser):
    def __init__(self, name='base', password: str = 'base'):
        self._message: str = ''
        self._name = name
        self._password: str = PasswordManager.hash_password(password)

    @property
    def name(self) -> str:
        return self._name

    def validate_password(self, password: str) -> bool:
        return self._password == PasswordManager.hash_password(password)

    def hash_password(self, password: str) -> str:
        return self._password

    @property
    def message(self) -> str:
        return self._message

    def can_edit_text(self) -> bool: ...

    def can_change_document_settings(self) -> bool: ...

    def update(self, document) -> None:
        self._message = f'Document updated: {datetime.datetime.now()}'


class EditorUser(User):
    def can_edit_text(self) -> bool:
        return True

    def can_change_document_settings(self) -> bool:
        return False


class ReaderUser(User):
    def can_edit_text(self) -> bool:
        return False

    def can_change_document_settings(self) -> bool:
        return False


class Admin(User):
    def can_edit_text(self) -> bool:
        return True

    def can_change_document_settings(self) -> bool:
        return True
