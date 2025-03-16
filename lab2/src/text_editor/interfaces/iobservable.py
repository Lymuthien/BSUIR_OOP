from abc import ABC, abstractmethod


class IObservable(ABC):
    @abstractmethod
    def attach(self, observer) -> None: ...

    @abstractmethod
    def detach(self, observer) -> None: ...

    @abstractmethod
    def notify(self) -> None: ...


class IObserver(ABC):
    @abstractmethod
    def update(self, document) -> None: pass