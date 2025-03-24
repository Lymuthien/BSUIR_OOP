import datetime
from abc import abstractmethod

from .documents.document import Document
from ..interfaces import IUser


class User(IUser):
    def __init__(self):
        self._message: str = ''

    @property
    def message(self) -> str:
        return self._message

    @abstractmethod
    def can_edit_text(self) -> bool: ...

    @abstractmethod
    def can_change_document_settings(self) -> bool: ...

    def update(self, document: Document) -> None:
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
