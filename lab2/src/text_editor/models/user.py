import datetime

from ..interfaces import IUser
from .registrable import Registrable


class User(IUser, Registrable):
    def __init__(self, name='base'):
        self._message: str = ''
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def message(self) -> str:
        return self._message

    def can_edit_text(self) -> bool: ...

    def can_change_document_settings(self) -> bool: ...

    def update(self, message: str) -> None:
        self._message = message

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'message': self._message,
            'name': self.name,
        }

    def from_dict(self,
                  data: dict) -> IUser:
        self._name = data['name']
        self._message = data['message']
        return self


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
