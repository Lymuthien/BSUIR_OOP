from abc import ABC, abstractmethod


class IEventBus(ABC):
    @abstractmethod
    def on(self, event_type: str, callback: callable):
        pass

    @abstractmethod
    def off(self, event_type: str, callback: callable):
        pass

    @abstractmethod
    def emit(self, event_type: str, *data):
        pass