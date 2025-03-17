from ...interfaces.iobservable import IObservable, IObserver
from ...interfaces.iserializer import IDictable
from ..text_component import TextComponent


class Document(IObservable, IDictable):
    def __init__(self):
        self._components: list[TextComponent] = []
        self.__observers: list[IObserver] = []

    def insert_text(self, text: str, position: int) -> None:
        current_text = self.get_text()
        new_text = current_text[:position] + text + current_text[position:]

        self._components = [TextComponent(new_text)]
        self.notify()

    def get_text(self) -> str:
        return ''.join(component.get_text() for component in self._components)

    def attach(self, observer: IObserver) -> None:
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self, observer: IObserver) -> None:
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify(self) -> None:
        for observer in self.__observers:
            observer.update(self)

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'components': [component.to_dict() for component in self._components]
        }

    def from_dict(self, data: dict) -> 'Document':
        raise NotImplementedError("Subclasses must implement from_dict")
