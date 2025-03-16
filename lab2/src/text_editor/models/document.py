from ..interfaces.iobservable import IObservable, IObserver
from abc import abstractmethod


class Document(IObservable):
    def __init__(self):
        self.__components = []
        self.__observers = []

    def get_text(self) -> str:
        return ''.join(component.get_text() for component in self.__components)

    def get_formatted_text(self) -> str:
        return ''.join(component.get_formatted_text() for component in self.__components)

    def attach(self, observer: IObserver) -> None:
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self, observer) -> None:
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify(self) -> None:
        for observer in self.__observers:
            observer.update(self)

    @abstractmethod
    def serialize(self, format_):
        pass

    @abstractmethod
    def deserialize(self, data, format_):
        pass
