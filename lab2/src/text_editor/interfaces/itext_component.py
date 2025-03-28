from abc import abstractmethod

from .iserializer import IDictable


class ITextComponent(IDictable):
    @abstractmethod
    def get_text(self) -> str: ...

