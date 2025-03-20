import hashlib

from ..theme import Theme
from ..settings import Settings
from ..text_component import TextComponent
from ...interfaces import IObserver, IObservable, IDictable


class Document(IObservable, IDictable):
    def __init__(self):
        self._components: list[TextComponent] = []
        self.__observers: list[IObserver] = []
        self._settings: Settings = Settings()

    def set_password(self, password: str):
        if self._settings.hash_password is None:
            self._settings.hash_password = self.__hash_password(password)
        else:
            raise Exception('Password is already set')

    @staticmethod
    def __hash_password(password: str) -> str:
        """Generate secure hash from plain text password."""

        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    def validate_password(self, password: str) -> bool:
        return self.__hash_password(password) == self._settings.hash_password

    def set_theme(self,
                  theme: Theme):
        self._settings.set_theme(theme)

    @property
    def settings(self):
        return self._settings

    def insert_text(self,
                    text: str,
                    position: int) -> None:
        current_text = self.get_text()
        new_text = current_text[:position] + text + current_text[position:]

        self._components = [TextComponent(new_text)]
        self.notify()

    def replace_text(self,
                     new_text: str,
                     start: int,
                     end: int) -> None:
        current_text = self.get_text()
        new_text = current_text[:start] + new_text + current_text[end + 1:]

        self._components = [TextComponent(new_text)]
        self.notify()

    def delete_text(self,
                    start: int,
                    end: int) -> None:
        current_text = self.get_text()
        new_text = current_text[:start] + current_text[end + 1:]

        self._components = [TextComponent(new_text)]
        self.notify()

    def clear(self) -> None:
        self._components = []
        self.notify()

    def get_text(self) -> str:
        return ''.join(component.get_text() for component in self._components)

    def attach(self,
               observer: IObserver) -> None:
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self,
               observer: IObserver) -> None:
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify(self) -> None:
        for observer in self.__observers:
            observer.update(self)

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'components': [component.to_dict() for component in self._components],
            'settings': self._settings.to_dict()
        }

    def from_dict(self,
                  data: dict) -> 'Document':
        raise NotImplementedError("Subclasses must implement from_dict")
