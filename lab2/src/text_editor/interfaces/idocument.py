from abc import abstractmethod

from .iobservable import IObservable
from .iserializer import IDictable


class IDocument(IObservable, IDictable):
    @abstractmethod
    def set_theme(self,
                  theme): ...

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
