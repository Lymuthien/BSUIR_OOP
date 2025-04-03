import datetime

from ..theme import Theme
from ...factories.text_component_factory import TextComponentFactory, BasicTextComponentFactory
from ...interfaces import ITextComponent, IUser
from ...interfaces.idocument import IDocument


class Document(IDocument):
    def __init__(self):
        self._components: list[ITextComponent] = []
        self._users: dict[str: IUser] = {}
        self._basic_factory: TextComponentFactory = BasicTextComponentFactory()

    def set_theme(self,
                  theme: Theme):
        self.notify()

    def insert_text(self,
                    text: str,
                    position: int) -> None:
        current_text = self.get_text()
        new_text = current_text[:position] + text + current_text[position:]

        self._components = [self._basic_factory.create_text_component(new_text)]
        self.notify()

    def replace_text(self,
                     new_text: str,
                     start: int,
                     end: int) -> None:
        current_text = self.get_text()
        new_text = current_text[:start] + new_text + current_text[end + 1:]

        self._components = [self._basic_factory.create_text_component(new_text)]
        self.notify()

    def delete_text(self,
                    start: int,
                    end: int) -> None:
        current_text = self.get_text()
        new_text = current_text[:start] + current_text[end + 1:]

        self._components = [self._basic_factory.create_text_component(new_text)]
        self.notify()

    def get_text(self) -> str:
        return ''.join(component.get_text() for component in self._components)

    def get_role(self,
                 name: str) -> IUser:
        return self._users.get(name)

    def set_role(self,
                 user: IUser) -> None:
        self._users[user.name] = user
        user.update(f'Your role now: {user.__class__.__name__}')

    def attach(self,
               observer: IUser) -> None:
        self._users[observer.name] = observer

    def detach(self,
               observer: IUser) -> None:
        if observer.name in self._users:
            del self._users[observer.name]

    def notify(self, message: str = None) -> None:
        for observer in self._users.values():
            observer.update(f'Document updated: {datetime.datetime.now()}' if message is None else message)

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
        from ...factories.user_factory import users

        self._components = [self._basic_factory.create_text_component(component['text'])
                            for component in data['components']]
        self._users = {}

        if isinstance(data['users'][0], list):
            data['users'] = data['users'][0]
        for user_data in data['users']:
            type_name = user_data['type'].lower()
            user = users[type_name].create_user().from_dict(user_data)
            self._users[user.name] = user

        return self
