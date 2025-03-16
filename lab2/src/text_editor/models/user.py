from abc import abstractmethod
from ..interfaces.iobservable import IObserver


class User(IObserver):
    @abstractmethod
    def can_edit_text(self) -> bool: ...

    @abstractmethod
    def can_change_document_settings(self) -> bool: ...

    def update(self, document) -> None:
        print(f"Document updated: \n'{document.get_formatted_text()}'")


class Editor(User):
    def can_edit_text(self) -> bool:
        return True

    def can_change_document_settings(self) -> bool:
        return False


class Reader(User):
    def can_edit_text(self) -> bool:
        return False

    def can_change_document_settings(self) -> bool:
        return False


class Admin(User):
    def can_edit_text(self) -> bool:
        return True

    def can_change_document_settings(self) -> bool:
        return True
