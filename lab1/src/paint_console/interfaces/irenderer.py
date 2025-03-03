from abc import ABC, abstractmethod
from .ifigure import IFigure, IDrawable


class IRenderStrategy(ABC):
    @staticmethod
    @abstractmethod
    def render(figure: IFigure, background: str) -> list[list[str]]:
        pass


class IRenderer(ABC):
    @staticmethod
    @abstractmethod
    def render(figure: IDrawable, x: int, y: int, grid: list[list[str]]) -> list[list[str]]:
        pass

class ICanvasRenderer(ABC):
    @staticmethod
    @abstractmethod
    def render(width: int, grid: tuple[tuple[str, ...], ...]):
        pass
