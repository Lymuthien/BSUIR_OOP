from abc import abstractmethod

from .iobservable import IObservable
from .iserializer import IDictable


class IDocument(IObservable, IDictable):
    @abstractmethod
    def set_password(self, password: str): ...

    @abstractmethod
    def validate_password(self, password: str) -> bool: ...

    @abstractmethod
    def set_theme(self,
                  theme): ...

    @property
    @abstractmethod
    def settings(self): ...

    @abstractmethod
    def insert_text(self,
                    text: str,
                    position: int) -> None: ...

    @abstractmethod
    def replace_text(self,
                     new_text: str,
                     start: int,
                     end: int) -> None: ...

    @abstractmethod
    def delete_text(self,
                    start: int,
                    end: int) -> None: ...

    @abstractmethod
    def get_text(self) -> str: ...
