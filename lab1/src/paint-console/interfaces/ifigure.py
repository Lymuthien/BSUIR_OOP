from abc import ABC, abstractmethod


class IFigure(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        pass

    @property
    @abstractmethod
    def type(self) -> str:
        pass


class IDrawable(ABC):
    @property
    @abstractmethod
    def background(self) -> str:
        pass

    @background.setter
    @abstractmethod
    def background(self, value: str):
        pass

    @abstractmethod
    def render(self) -> list[list[str]]:
        pass


class INavigator(ABC):
    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def prev(self):
        pass

    @property
    @abstractmethod
    def current(self):
        pass
