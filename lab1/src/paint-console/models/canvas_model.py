from copy import copy
from uuid import uuid4
from typing import Generator
from ..interfaces import IFigure, ICanvasModel, IFigureLayout, ICanvasView, IRenderer, IDrawable


class FigureLayout(IFigureLayout):
    def __init__(self, figure: IDrawable, coordinates: tuple[float, float], layer: int):
        self.__figure = figure
        self.coordinates = coordinates
        self.layer = layer

    @property
    def figure(self) -> IDrawable:
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


class CanvasModel(ICanvasModel):
    def __init__(self):
        self.__figures: dict[str, FigureLayout] = {}

    def add_figure(self, figure: IDrawable, x: float, y: float, layer: int = 0, figure_id: str = None) -> str:
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

    def get_all_figures(self) -> Generator[tuple[str, FigureLayout]]:
        for figure_id, layout in self.__figures.items():
            yield figure_id, layout


class CanvasView(ICanvasView):
    def __init__(self, model: ICanvasModel, renderer: IRenderer, width: int = 100, height: int = 30
    ):
        self.__model = model
        self.__renderer = renderer
        self.__grid = [[''] * width for _ in range(height)]

    def draw_figure(self, figure: IDrawable, x: int, y: int) -> None:
        self.__renderer.render(figure, x, y, figure.background,self.__grid)

    def clear(self) -> None:
        for row in self.__grid:
            for i in range(len(row)):
                row[i] = ''

    def update(self) -> None:
        self.clear()
        for figure, layout in self.__model.get_all_figures():
            self.draw_figure(layout.figure, layout.coordinates[0], layout.coordinates[1])

    @property
    def grid(self) -> tuple[tuple[str, ...], ...]:
        return tuple(tuple(row) for row in self.__grid)
