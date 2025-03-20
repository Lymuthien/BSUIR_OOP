from abc import abstractmethod

from .documents.document import Document
from ..interfaces import IObserver


class User(IObserver):
    @abstractmethod
    def can_edit_text(self) -> bool: ...

    @abstractmethod
    def can_change_document_settings(self) -> bool: ...

    def update(self, document: Document) -> None:
        return
        print(f"Document updated: \n'{document.get_text()}'")


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
