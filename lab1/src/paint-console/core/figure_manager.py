from interfaces import INavigator


class FigureNavigator(INavigator):
    def __init__(self):
        self.__figures = []
        self.__current_index = 0

    def add(self, figure):
        self.__figures.append(figure)

    def remove(self, figure):
        if figure in self.__figures:
            self.__figures.remove(figure)

    def next(self):
        if not self.__figures:
            return
        self.__current_index = (self.current_index + 1) % len(self.figures)

    def prev(self):
        if not self.__figures:
            return
        self.__current_index = (self.current_index - 1) % len(self.figures)

    @property
    def current(self):
        if not self.__figures:
            return
        return self.__figures[self.__current_index]
