class Theme(object):
    def __init__(self, theme_name: str, font_size: int, italic: bool, bald: bool):
        self.__theme_name = theme_name
        self.__font_size = font_size
        self.__italic = italic
        self.__bald = bald

    @property
    def theme_name(self):
        return self.__theme_name

    @property
    def font_size(self):
        return self.__font_size

    @property
    def italic(self):
        return self.__italic

    @property
    def bald(self):
        return self.__bald
