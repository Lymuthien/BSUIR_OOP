from abc import ABC, abstractmethod
from .figure import Figure


class RenderStrategy(ABC):
    @abstractmethod
    def render(self, figure: Figure, background: str) -> list[list[str]]:
        pass
