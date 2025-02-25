from abc import ABC, abstractmethod
from .figure import Figure, Drawable


class RenderStrategy(ABC):
    @abstractmethod
    def render(self, figure: Figure, background: str) -> list[list[str]]:
        pass


class Renderer(ABC):
    @abstractmethod
    def render(self, figure: Drawable, x: int, y: int, background: str, grid: list[list[str]]):
        pass
