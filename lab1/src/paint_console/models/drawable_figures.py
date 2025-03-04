from ..interfaces import IDrawable
from ..utils import EllipseMath, RectangleMath, TriangleMath
from ..renderers import EllipseRenderer, RectangleRenderer, TriangleRenderer
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
        self.__background = background
        self.__renderer = EllipseRenderer()

    def render(self) -> list[list[str]]:
        """Represent the ellipse as a list of lines."""
        return self.__renderer.render(self, self.__background)

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
        self.__background = background
        self.__renderer = RectangleRenderer()

    def render(self) -> list[list[str]]:
        """Represent the rectangle as a list of lines."""
        return self.__renderer.render(self, self.__background)

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
        self.__background = background
        self.__renderer = TriangleRenderer()

    def render(self) -> list[list[str]]:
        """Represent the triangle as a list of lines."""
        return self.__renderer.render(self, self.__background)

    @property
    def info(self) -> dict:
        """Give all info about the triangle."""
        return {
            **super().info,
            **super(TriangleMath, self).info
        }
