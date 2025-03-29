class EditorSettings(object):
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not EditorSettings._initialized:
            self.__font_size = 11
            self.__font_sizes = (9, 10, 11, 12, 13, 14)
            EditorSettings._initialized = True

    @property
    def font_size(self) -> int:
        return self.__font_size

    @font_size.setter
    def font_size(self, font_size: int):
        if font_size in self.__font_sizes:
            self.__font_size = font_size

    @property
    def font_sizes(self) -> tuple:
        return self.__font_sizes
