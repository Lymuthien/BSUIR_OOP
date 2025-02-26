from abc import ABC, abstractmethod
from typing import Generator
from .ifigure import IDrawable


class IFigureLayout(ABC):
    @property
    @abstractmethod
    def figure(self) -> IDrawable:
        pass

    @property
    @abstractmethod
    def coordinates(self) -> tuple:
        pass

    @coordinates.setter
    @abstractmethod
    def coordinates(self, coordinates: tuple):
        pass

    @property
    @abstractmethod
    def layer(self):
        pass


class ICanvasModel(ABC):
    @abstractmethod
    def add_figure(self, figure: IDrawable, x: float, y: float, layer: int = 0, figure_id: str = None) -> str:
        pass

    @abstractmethod
    def remove_figure(self, figure_id: str):
        pass

    @abstractmethod
    def get_figure_layout(self, figure_id: str) -> IFigureLayout:
        pass

    @abstractmethod
    def get_all_figures(self) -> Generator[tuple[str, IFigureLayout], None, None]:
        pass


class ISearching(ABC):
    @abstractmethod
    def search(self, obj):
        pass


class ICanvasView(ABC):
    @abstractmethod
    def draw_figure(self, figure: IDrawable, x: int, y: int) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @property
    @abstractmethod
    def grid(self) -> tuple[tuple[str]]:
        pass


class ISearchingCanvasModel(ICanvasModel, ISearching, ABC):
    pass
