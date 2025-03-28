from abc import abstractmethod

from . import IDictable
from .iobservable import IObserver


class IUser(IObserver, IDictable):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def can_edit_text(self) -> bool: ...

    @abstractmethod
    def can_change_document_settings(self) -> bool: ...

    @abstractmethod
    def validate_password(self, password: str) -> bool: ...

    @abstractmethod
    def hash_password(self, password: str) -> str: ...

