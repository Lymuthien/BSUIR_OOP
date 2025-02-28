from copy import copy, deepcopy
from uuid import uuid4
from typing import Generator
from interfaces import ICanvasModel, IFigureLayout, ICanvasView, IRenderer, IDrawable, ISearchingCanvasModel, \
    INavigator


class Navigator(INavigator):
    def __init__(self):
        self.__objects = []
        self.__current_index = -1

    def append(self, item):
        self.__objects.append(item)
        self.__current_index = self.__objects.index(item)

    def remove(self, item):
        if item in self.__objects:
            self.__objects.remove(item)
            if len(self.__objects):
                self.prev()
            else:
                self.__current_index = -1

    def next(self):
        if self.__current_index != -1:
            self.__current_index = (self.__current_index + 1) % len(self.__objects)
            return self.__objects[self.__current_index]

    def prev(self):
        if self.__current_index != -1:
            self.__current_index = (self.__current_index - 1) % len(self.__objects)
            return self.__objects[self.__current_index]

    def current(self):
        if self.__current_index != -1:
            return self.__objects[self.__current_index]


class FigureLayout(IFigureLayout):
    def __init__(self, figure: IDrawable, coordinates: tuple[float, float], layer: int):
        self.__figure = figure
        self.coordinates = coordinates
        self.__layer = layer

    @property
    def figure(self) -> IDrawable:
        return self.__figure

    @property
    def coordinates(self) -> tuple:
        return copy(self.__coordinates)

    @coordinates.setter
    def coordinates(self, coordinates: tuple):
        self.__coordinates = coordinates

    @property
    def layer(self):
        return self.__layer


class CanvasModel(ISearchingCanvasModel):
    def __init__(self):
        self.__figures: dict[str, FigureLayout] = {}
        self.__navigator = Navigator()

    def add_figure(self, figure: IDrawable, x: float, y: float, layer: int = 0, figure_id: str = None) -> str:
        if figure_id is None:
            figure_id = str(uuid4())
        self.__figures[figure_id] = FigureLayout(figure, (x, y), layer)
        self.__navigator.append(figure)
        self._filter()
        return figure_id

    @property
    def navigator(self):
        return self.__navigator

    @property
    def get_data(self):
        return deepcopy(self.__figures)

    def load_data(self, data: dict):
        self.__figures = data
        for layout in self.__figures.values():
            self.__navigator.append(layout.figure)

    def remove_figure(self, figure_id: str):
        self.__navigator.remove(self.__figures[figure_id].figure)
        self.__figures.pop(figure_id)

    def get_figure_layout(self, figure_id: str) -> FigureLayout:
        if figure_id not in self.__figures:
            raise KeyError("No such figure")
        return self.__figures[figure_id]

    def get_all_figures(self) -> Generator[tuple[str, FigureLayout], None, None]:
        for figure_id, layout in self.__figures.items():
            yield figure_id, layout

    def search(self, obj: IDrawable, start: int = 0) -> str:
        for figure_id, layout in self.__figures.items():
            if start > 0:
                start = start - 1
                continue
            if layout.figure == obj:
                return figure_id

    def _filter(self):
        self.__figures = dict(sorted(self.__figures.items(), key=lambda item: item[1].layer))


class CanvasView(ICanvasView):
    def __init__(self, model: ICanvasModel, renderer: IRenderer, width: int = 80, height: int = 30
                 ):
        self.__model = model
        self.__renderer = renderer
        self.__width = width
        self.__grid = [[' '] * width for _ in range(height)]

    @property
    def width(self) -> int:
        return self.__width

    def draw_figure(self, figure: IDrawable, x: int, y: int) -> None:
        self.__renderer.render(figure, x, y, self.__grid)

    def clear(self) -> None:
        for row in self.__grid:
            for i in range(len(row)):
                row[i] = ' '

    def update(self) -> None:
        self.clear()
        for figure, layout in self.__model.get_all_figures():
            self.draw_figure(layout.figure, layout.coordinates[0], layout.coordinates[1])

    @property
    def grid(self) -> tuple[tuple[str, ...], ...]:
        return tuple(tuple(row) for row in self.__grid)
