from ..utils.singleton import singleton
from ..models.theme import Theme


@singleton
class Settings(object):
    def __init__(self):
        self.__font_size: int = 4
        self.__all_bald: bool = False
        self.__all_italic: bool = False

    @property
    def font_size(self):
        return self.__font_size

    @font_size.setter
    def font_size(self, value: int):
        self.__font_size = value

    @property
    def all_bald(self):
        return self.__all_bald

    @all_bald.setter
    def all_bald(self, value: bool):
        self.__all_bald = value

    @property
    def all_italic(self):
        return self.__all_italic

    @all_italic.setter
    def all_italic(self, value: bool):
        self.__all_italic = value

    def set_theme(self, theme: Theme):
        self.__font_size = theme.font_size
        self.__all_bald = theme.bald
        self.__all_italic = theme.italic



