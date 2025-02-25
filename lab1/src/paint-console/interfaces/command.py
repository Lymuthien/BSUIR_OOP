from abc import ABC, abstractmethod
from . import EventBus


class Command(ABC):
    @abstractmethod
    def undo(self, event_bus: EventBus):
        pass

    @abstractmethod
    def redo(self, event_bus: EventBus):
        pass
