from abc import ABC, abstractmethod


class IObserver(ABC):
    @abstractmethod
    def update(self,
               data) -> None: ...


class IObservable(ABC):
    @abstractmethod
    def attach(self,
               observer: IObserver) -> None: ...

    @abstractmethod
    def detach(self,
               observer: IObserver) -> None: ...

    @abstractmethod
    def notify(self) -> None: ...
