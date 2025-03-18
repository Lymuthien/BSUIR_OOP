from abc import ABC, abstractmethod

class ITextComponent(ABC):
    @abstractmethod
    def get_text(self) -> str: ...