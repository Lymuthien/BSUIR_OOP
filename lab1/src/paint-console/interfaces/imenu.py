from abc import ABC, abstractmethod

class IMenuItem(ABC):
    @abstractmethod
    def execute(self):
        pass

class IAddableMenu(IMenuItem):
    @abstractmethod
    def add_item(self, key: str, item: IMenuItem):
        pass