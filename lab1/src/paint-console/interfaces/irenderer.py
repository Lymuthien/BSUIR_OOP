from abc import ABC, abstractmethod
from .ifigure import IFigure, IDrawable


class IRenderStrategy(ABC):
    @abstractmethod
    def render(self, figure: IFigure, background: str) -> list[list[str]]:
        pass


class IRenderer(ABC):
    @abstractmethod
    def render(self, figure: IDrawable, x: int, y: int, background: str, grid: list[list[str]]):
        pass
