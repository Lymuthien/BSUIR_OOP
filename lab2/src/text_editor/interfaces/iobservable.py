from abc import ABC, abstractmethod


class IObservable(ABC):
    @abstractmethod
    def attach(self, observer): ...

    @abstractmethod
    def detach(self, observer): ...

    @abstractmethod
    def notify(self): ...


class IObserver(ABC):
    @abstractmethod
    def update(self, document): pass