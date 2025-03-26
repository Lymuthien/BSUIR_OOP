from abc import abstractmethod

from .iobservable import IObserver


class IUser(IObserver):
    @abstractmethod
    def can_edit_text(self) -> bool: ...

    @abstractmethod
    def can_change_document_settings(self) -> bool: ...
