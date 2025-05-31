from abc import ABC, abstractmethod

from .ifigure import IDrawable


class IRenderer(ABC):
    @staticmethod
    @abstractmethod
    def render(
        figure: IDrawable, x: int, y: int, grid: list[list[str]]
    ) -> list[list[str]]:
        pass


class ICanvasRenderer(ABC):
    @staticmethod
    @abstractmethod
    def render(width: int, grid: tuple[tuple[str, ...], ...]):
        pass
