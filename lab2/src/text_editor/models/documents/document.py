from ..text_component import TextComponent
from ..theme import Theme
from ..user import User
from ...interfaces import ITextComponent, IUser
from ...interfaces.idocument import IDocument


class Document(IDocument):
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__.lower()] = cls

    @classmethod
    def registry(cls) -> dict:
        return cls._registry

    def __init__(self):
        self._components: list[ITextComponent] = []
        self._users: dict[str: IUser] = {}

    def set_theme(self,
                  theme: Theme):
        self.notify()

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

    def get_role(self,
                 name: str) -> IUser:
        return self._users.get(name)

    def attach(self,
               observer: IUser) -> None:
        self._users[observer.name] = observer
        # мб тут если он уже есть в юзере оповещать о смене роли

    def detach(self,
               observer: IUser) -> None:
        if observer.name in self._users:
            del self._users[observer.name]

    def notify(self) -> None:
        for observer in self._users.values():
            observer.update(self)

    def users(self) -> dict[str: IUser]:
        return self._users

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'components': [component.to_dict() for component in self._components],
            'users': [user.to_dict() for user in self._users.values()],
        }

    def from_dict(self,
                  data: dict) -> 'Document':
        self._components = [TextComponent(component['text']) for component in data['components']]
        self._users = {}

        for user_data in data['users']:
            user_type = user_data['type'].lower()
            user_class = User.registry().get(user_type)
            if user_class:
                user = user_class().from_dict(user_data)
                self._users[user.name] = user
            else:
                raise ValueError(f'Unknown user role: {user_type}')

        return self

