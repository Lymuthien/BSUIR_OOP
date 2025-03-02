from copy import copy, deepcopy
from uuid import uuid4
from typing import Generator
from ..interfaces import ICanvasModel, IFigureLayout, ICanvasView, IRenderer, IDrawable, ISearchingCanvasModel, \
    INavigator


class FigureLayout(IFigureLayout):
    def __init__(self, figure: IDrawable, coordinates: tuple[float, float], layer: int):
        """Layout consisting all information about a figure and its environment."""
        self._validate_layer(layer)
        self.__figure = figure
        self.coordinates = coordinates
        self.__layer = layer

    @property
    def figure(self) -> IDrawable:
        """Return the figure object."""
        return self.__figure

    @property
    def coordinates(self) -> tuple:
        """Return figure coordinates in environment."""
        return copy(self.__coordinates)

    @coordinates.setter
    def coordinates(self, coordinates: tuple):
        self.__coordinates = coordinates

    @property
    def layer(self):
        """Return figure layer in environment."""
        return self.__layer

    @property
    def info(self) -> dict:
        """Return info about the figure and its environment."""
        return {
            **self.__figure.info,
            'coordinates': self.coordinates,
            'layer': self.layer
        }

    @staticmethod
    def _validate_layer(layer: int):
        if layer < 0:
            raise ValueError('Layer must be non-negative')


class CanvasModel(ISearchingCanvasModel):
    def __init__(self, navigator: INavigator):
        self.__figures: dict[str, FigureLayout] = {}
        self.__navigator = navigator

    def add_figure(self, figure: IDrawable, x: float, y: float, layer: int = 0, figure_id: str = None) -> str:
        """
        Add a figure with it environment to the store.
        :return: id of the added figure.
        """
        if figure_id is None:
            figure_id = str(uuid4())
        self.__figures[figure_id] = FigureLayout(figure, (x, y), layer)
        self.__navigator.append(figure)
        self._filter()
        return figure_id

    def remove_figure(self, figure_id: str):
        """Remove a figure from the store by id."""
        self.__navigator.remove(self.__figures[figure_id].figure)
        self.__figures.pop(figure_id)

    def get_current_info(self) -> dict:
        """Give current info about the figure and its environment."""
        figure = self.__navigator.current()
        figure_id = self.search(figure)
        return self.__figures[figure_id].info

    def new_layer(self) -> int:
        """Return number for new max layer in the store."""
        return max((layout.layer for layout in self.__figures.values()), default=-1) + 1

    @property
    def navigator(self):
        """Return the navigator object."""
        return self.__navigator

    @property
    def get_data(self):
        """Give copy of all data"""
        return deepcopy(self.__figures)

    def load_data(self, data: dict):
        """Load copy of all data"""
        self.__figures = deepcopy(data)
        for layout in self.__figures.values():
            self.__navigator.append(layout.figure)

    def get_figure_layout(self, figure_id: str) -> FigureLayout:
        """Return the figure layout by id."""
        if figure_id not in self.__figures:
            raise KeyError("No such figure")
        return self.__figures[figure_id]

    def get_all_figures(self) -> Generator[FigureLayout, None, None]:
        """Return all figure layouts."""
        yield from self.__figures.values()

    def search(self, obj: IDrawable, start: int = 0) -> str | None:
        """Give object id in the store if it exists."""
        for figure_id, layout in self.__figures.items():
            if start > 0:
                start = start - 1
                continue
            if layout.figure == obj:
                return figure_id

    def _filter(self):
        self.__figures = dict(sorted(self.__figures.items(), key=lambda item: item[1].layer))


class CanvasView(ICanvasView):
    def __init__(self, model: ICanvasModel, renderer: IRenderer, width: int = 80, height: int = 30):
        """Visual part of the canvas."""
        self.__model = model
        self.__renderer = renderer
        self.__width = width
        self.__height = height
        self.__grid = [[' '] * width for _ in range(height)]

    @property
    def width(self) -> int:
        """Width of the canvas."""
        return self.__width

    @property
    def height(self) -> int:
        """Height of the canvas."""
        return self.__height

    def draw_figure(self, figure: IDrawable, x: int, y: int) -> None:
        """Draw the figure."""
        self.__grid = self.__renderer.render(figure, x, y, self.__grid)

    def clear(self) -> None:
        """Clear the canvas."""
        self.__grid = [[' '] * self.width for _ in range(self.height)]

    def update(self) -> None:
        """Update the canvas."""
        self.clear()
        for layout in self.__model.get_all_figures():
            self.draw_figure(layout.figure, layout.coordinates[0], layout.coordinates[1])

    @property
    def grid(self) -> tuple[tuple[str, ...], ...]:
        """Return the visual grid."""
        return tuple(tuple(row) for row in self.__grid)
