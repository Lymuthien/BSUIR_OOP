from copy import copy
from uuid import uuid4
from typing import Generator

from ..interfaces import Figure


class FigureLayout:
    def __init__(self, figure: Figure, coordinates: tuple[float, float], layer: int):
        self.__figure = figure
        self.coordinates = coordinates
        self.layer = layer

    @property
    def figure(self) -> Figure:
        return copy(self.__figure)

    @property
    def coordinates(self) -> tuple:
        return copy(self.__coordinates)

    @coordinates.setter
    def coordinates(self, coordinates: tuple):
        self.__coordinates = coordinates

    @property
    def layer(self):
        return self.__layer

    @layer.setter
    def layer(self, layer: int):
        self._validate_layer(layer)
        self.__layer = layer

    @staticmethod
    def _validate_layer(layer: int):
        if layer < 0:
            raise ValueError("Layer cannot be negative")


class CanvasModel:
    def __init__(self):
        self.__figures: dict[str, FigureLayout] = {}

    def add_figure(self, figure: Figure, x: float, y: float, layer: int = 0, figure_id: str = None) -> str:
        if figure_id is None:
            figure_id = str(uuid4())
        self.__figures[figure_id] = FigureLayout(figure, (x, y), layer)
        return figure_id

    def remove_figure(self, figure_id: str):
        self.__figures.pop(figure_id)

    def get_figure_layout(self, figure_id: str) -> FigureLayout:
        if figure_id not in self.__figures:
            raise KeyError("No such figure")
        return self.__figures[figure_id]

    def get_all_figures(self) -> Generator[tuple[Figure, tuple, int, str], None, None]:
        for figure_id, layout in self.__figures.items():
            yield layout.figure, layout.coordinates, layout.layer, figure_id
