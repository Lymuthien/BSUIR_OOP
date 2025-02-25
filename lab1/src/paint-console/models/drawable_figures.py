from interfaces import Drawable
from mathematics import EllipseMath, RectangleMath, TriangleMath
from renderers import EllipseRenderer, RectangleRenderer, TriangleRenderer
from abc import abstractmethod


class DrawableFigure(Drawable):
    def __init__(self, background: str):
        self.background = background

    @property
    def background(self) -> str:
        return self._background

    @background.setter
    def background(self, background: str):
        self._validate_background(background)
        self._background = background

    @staticmethod
    def _validate_background(background: str):
        if len(background) != 1:
            raise ValueError('Background must be a single character')

    @abstractmethod
    def render(self) -> list[list[str]]:
        pass


class DrawableEllipse(EllipseMath, DrawableFigure):
    def __init__(self, vertical_radius: float, horizontal_radius: float, background: str):
        DrawableFigure.__init__(self, background)
        EllipseMath.__init__(self, vertical_radius, horizontal_radius)
        self._background = background
        self._renderer = EllipseRenderer()

    def render(self) -> list[list[str]]:
        return self._renderer.render(self, self._background)


class DrawableRectangle(RectangleMath, DrawableFigure):
    def __init__(self, width: float, height: float, background: str):
        DrawableFigure.__init__(self, background)
        RectangleMath.__init__(self, width, height)
        self._background = background
        self._renderer = RectangleRenderer()

    def render(self) -> list[list[str]]:
        return self._renderer.render(self, self._background)


class DrawableTriangle(TriangleMath, DrawableFigure):
    def __init__(self, vertices: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
                 background: str):
        DrawableFigure.__init__(self, background)
        TriangleMath.__init__(self, vertices)
        self._background = background
        self._renderer = TriangleRenderer()

    def render(self) -> list[list[str]]:
        return self._renderer.render(self, self._background)
