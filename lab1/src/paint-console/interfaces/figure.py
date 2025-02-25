from abc import ABC, abstractmethod


class Figure(ABC):
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


class Drawable(ABC):
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
