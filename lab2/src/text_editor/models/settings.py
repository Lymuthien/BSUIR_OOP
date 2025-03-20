from .theme import Theme
from ..utils.singleton import singleton


@singleton
class Settings(object):
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



