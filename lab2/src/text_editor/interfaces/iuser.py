from abc import abstractmethod

from .iserializer import IDictable
from .iobservable import IObserver


class IUser(IObserver, IDictable):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def can_edit_text(self) -> bool: ...

    @abstractmethod
    def can_change_document_settings(self) -> bool: ...

    @property
    @abstractmethod
    def message(self) -> str: ...
