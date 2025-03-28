from ..user import User, EditorUser, Admin, ReaderUser
from ..document_settings import DocumentSettings
from ..text_component import TextComponent
from ..theme import Theme
from ...interfaces import ITextComponent, IUser
from ...interfaces.idocument import IDocument


class Document(IDocument):
    def __init__(self):
        self._components: list[ITextComponent] = []
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
        self.__users[observer.name] = observer
        # мб тут если он уже есть в юзере оповещать о смене роли

    def detach(self,
               observer: IUser) -> None:
        if observer.name in self.__users:
            del self.__users[observer.name]

    def notify(self) -> None:
        for observer in self.__users.values():
            observer.update(self)

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'components': [component.to_dict() for component in self._components],
            'settings': self._settings.to_dict(),
            'users': {name: user.to_dict() for name, user in self.__users.items()},
        }

    def from_dict(self,
                  data: dict) -> 'Document':
        self._components = [TextComponent(component['text']) for component in data['components']]
        self._settings = self.settings.from_dict(data['settings'])
        self.__users = {}

        for name, user_data in data['users'].items():
            user_type = user_data['type'].lower()
            user_class = User.registry().get(user_type)
            if user_class:
                self.__users[name] = user_class().from_dict(user_data)
            else:
                raise ValueError(f'Unknown user role: {user_type}')

        return self

    # TODO: add user fabric

