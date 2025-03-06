import math

from ..interfaces import IDrawable
from ..utils import EllipseMath, RectangleMath, TriangleMath
from abc import abstractmethod


class DrawableFigure(IDrawable):
    def __init__(self, background: str):
        self.background = background

    @property
    def background(self) -> str:
        """Return the background symbol of the figure."""
        return self.__background

    @background.setter
    def background(self, background: str):
        self._validate_background(background)
        self.__background = background

    @staticmethod
    def _validate_background(background: str):
        if len(background) != 1:
            raise ValueError('Background must be a single character')

    @abstractmethod
    def render(self) -> list[list[str]]:
        pass

    @property
    def info(self) -> dict:
        return {
            'background': self.background,
        }


class DrawableEllipse(EllipseMath, DrawableFigure):
    def __init__(self, vertical_radius: float, horizontal_radius: float, background: str):
        """Ellipse that can be drawn and calculated"""
        DrawableFigure.__init__(self, background)
        EllipseMath.__init__(self, vertical_radius, horizontal_radius)

    def render(self) -> list[list[str]]:
        """Represent the ellipse as a list of lines."""
        vr = math.ceil(self.vertical_radius)
        hr = math.ceil(self.horizontal_radius)
        image = [[''] * (2 * hr) for _ in range(2 * vr)]

        for y in range(2 * vr):
            for x in range(2 * hr):
                dx = x - hr + 0.5
                dy = y - vr + 0.5
                if (dx ** 2) / (hr ** 2) + (dy ** 2) / (vr ** 2) <= 1:
                    image[y][x] = self.background
        return image

    @property
    def info(self) -> dict:
        """Give all info about the ellipse."""
        return {
            **super().info,
            **super(EllipseMath, self).info
        }


class DrawableRectangle(RectangleMath, DrawableFigure):
    def __init__(self, width: float, height: float, background: str):
        """Rectangle that can be drawn and calculated"""
        DrawableFigure.__init__(self, background)
        RectangleMath.__init__(self, width, height)

    def render(self) -> list[list[str]]:
        """Represent the rectangle as a list of lines."""
        return [[self.background] * int(self.width) for _ in range(int(self.height))]

    @property
    def info(self) -> dict:
        """Give all info about the rectangle."""
        return {
            **super().info,
            **super(RectangleMath, self).info,
        }


class DrawableTriangle(TriangleMath, DrawableFigure):
    def __init__(self, vertices: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
                 background: str):
        """Triangle that can be drawn and calculated"""
        DrawableFigure.__init__(self, background)
        TriangleMath.__init__(self, vertices)

    def render(self) -> list[list[str]]:
        """Represent the triangle as a list of lines."""
        max_x = int(max(x for x, y in self.vertices))
        max_y = int(max(y for x, y in self.vertices))
        image = [[''] * (max_x + 1) for _ in range(max_y + 1)]

        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if DrawableTriangle._is_point_inside(self.area, self.vertices, x, y):
                    image[y][x] = self.background
        return image

    @property
    def info(self) -> dict:
        """Give all info about the triangle."""
        return {
            **super().info,
            **super(TriangleMath, self).info
        }

    @staticmethod
    def _is_point_inside(basic_area, vertices, x, y) -> bool:
        """Check if areas of all triangles in sum gives basic area."""
        triangles_area = []
        for a, b in zip(vertices, vertices[1:] + vertices[:1]):
            try:
                triangles_area.append(TriangleMath((a, b, (x, y))).area)
            except ValueError:
                triangles_area.append(0)

        if sum(triangles_area) - basic_area < 1:
            return True
        return False
