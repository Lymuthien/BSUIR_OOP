from abc import ABC, abstractmethod

class ITextComponent(ABC):
    @abstractmethod
    def get_text(self) -> str: pass

    @abstractmethod
    def get_formatted_text(self) -> str: pass