from ..user import User, EditorUser, Admin, ReaderUser
from ..document_settings import DocumentSettings
from ..text_component import TextComponent
from ..theme import Theme
from ...interfaces import ITextComponent, IUser
from ...interfaces.idocument import IDocument


class Document(IDocument):
    def __init__(self):
        self._components: list[ITextComponent] = []
        self.__observers: list[IUser] = []
        self.__users: dict[str: IUser] = {}
        self._settings: DocumentSettings = DocumentSettings()

    def set_theme(self,
                  theme: Theme):
        self._settings.set_theme(theme)
        self.notify()

    @property
    def settings(self) -> DocumentSettings:
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

    def get_text(self) -> str:
        return ''.join(component.get_text() for component in self._components)

    def set_role(self,
                 name: str,
                 role: IUser) -> None:
        self.__users[name] = role

    def get_role(self,
                 name: str) -> IUser:
        return self.__users.get(name)

    def attach(self,
               observer: IUser) -> None:
        if observer not in self.__observers:
            self.__observers.append(observer)

    def detach(self,
               observer: IUser) -> None:
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify(self) -> None:
        for observer in self.__observers:
            observer.update(self)

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'components': [component.to_dict() for component in self._components],
            'settings': self._settings.to_dict(),
            'users': {name: user.to_dict() for name, user in self.__users.items()},
            'observers': [user.to_dict() for user in self.__observers],
        }

    def from_dict(self,
                  data: dict) -> 'Document':
        self._components = [TextComponent(component['text']) for component in data['components']]
        self._settings = self.settings.from_dict(data['settings'])
        self.__observers = [User().from_dict(observer) for observer in data['observers']]
        self.__users = {}
        for name, user in data['users'].items():
            if user['type'] == 'Admin':
                self.__users[name] = Admin().from_dict(user)
            elif user['type'] == 'EditorUser':
                self.__users[name] = EditorUser().from_dict(user)
            elif user['type'] == 'ReaderUser':
                self.__users[name] = ReaderUser().from_dict(user)

        return self

    # TODO: add user fabric

