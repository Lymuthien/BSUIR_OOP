from .theme import Theme
from ..utils.singleton import singleton
from ..interfaces import IDictable


@singleton
class Settings(IDictable):
    def __init__(self):
        self.__font_size: int = 4
        self.__all_bold: bool = False
        self.__all_italic: bool = False
        self.__read_only: bool = False
        self.__hash_password: str | None = None

    @property
    def read_only(self) -> bool:
        return self.__read_only

    @read_only.setter
    def read_only(self, value: bool):
        self.__read_only = value

    @property
    def hash_password(self) -> str:
        return self.__hash_password

    @hash_password.setter
    def hash_password(self, value: str):
        self.__hash_password = value

    @property
    def font_size(self) -> int:
        return self.__font_size

    @font_size.setter
    def font_size(self,
                  value: int):
        self.__font_size = value

    @property
    def all_bold(self) -> bool:
        return self.__all_bold

    @all_bold.setter
    def all_bold(self,
                 value: bool):
        self.__all_bold = value

    @property
    def all_italic(self) -> bool:
        return self.__all_italic

    @all_italic.setter
    def all_italic(self,
                   value: bool):
        self.__all_italic = value

    def set_theme(self,
                  theme: Theme):
        self.__font_size = theme.font_size
        self.__all_bold = theme.bold
        self.__all_italic = theme.italic

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'font_size': self.font_size,
            'all_bold': self.all_bold,
            'all_italic': self.all_italic,
            'read_only': self.read_only,
            'hash_password': self.hash_password,
        }

    def from_dict(self,
                  data: dict) -> 'Settings':
        self.__font_size = data['font_size']
        self.__all_bold = data['all_bold']
        self.__all_italic = data['all_italic']
        self.__read_only = data['read_only']
        self.__hash_password = data['hash_password']

        return self



