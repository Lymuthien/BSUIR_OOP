class Theme(object):
    def __init__(self,
                 font_size: int,
                 italic: bool = False,
                 bold: bool = False):
        self.__font_size = font_size
        self.__italic = italic
        self.__bold = bold

    @property
    def font_size(self):
        return self.__font_size

    @property
    def italic(self):
        return self.__italic

    @property
    def bold(self):
        return self.__bold
