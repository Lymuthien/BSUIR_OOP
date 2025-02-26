from abc import ABC, abstractmethod
from . import IEventBus


class ICommand(ABC):
    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        pass
