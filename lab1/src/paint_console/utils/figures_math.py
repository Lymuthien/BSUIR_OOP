from ..interfaces import IFigure
from math import pi, hypot, sqrt


class EllipseMath(IFigure):
    def __init__(self, vertical_radius: float, horizontal_radius: float):
        """Calculations for ellipse."""
        self.__validate_input(vertical_radius, horizontal_radius)
        self._vertical_radius = vertical_radius
        self._horizontal_radius = horizontal_radius

    @staticmethod
    def __validate_input(vertical_radius: float, horizontal_radius: float):
        if vertical_radius < 0 or horizontal_radius < 0:
            raise ValueError("Vertical radius and horizontal radius cannot be negative")

    @property
    def area(self) -> float:
        """Return the area of the ellipse."""
        return self._vertical_radius * self._horizontal_radius * pi

    @property
    def perimeter(self) -> float:
        """Return the perimeter of the ellipse."""
        return 2 * pi * sqrt((self._vertical_radius ** 2 + self._horizontal_radius ** 2) / 2)

    @property
    def vertical_radius(self) -> float:
        """Return the vertical radius of the ellipse."""
        return self._vertical_radius

    @property
    def horizontal_radius(self) -> float:
        """Return the horizontal radius of the ellipse."""
        return self._horizontal_radius

    @property
    def type(self) -> str:
        return 'ellipse'

    @property
    def info(self) -> dict:
        """Return all info about the ellipse."""
        return {
            'type': self.type,
            'vertical_radius': self.vertical_radius,
            'horizontal_radius': self.horizontal_radius,
            'area': self.area,
            'perimeter': self.perimeter,
        }


class RectangleMath(IFigure):
    def __init__(self, width: float, height: float):
        """Calculations for rectangle"""
        self.__validate_input(width, height)
        self._width = width
        self._height = height

    @staticmethod
    def __validate_input(width: float, height: float):
        if width < 0 or height < 0:
            raise ValueError("Width and height cannot be negative")

    @property
    def area(self) -> float:
        """Return the area of the rectangle."""
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        """Return the perimeter of the rectangle."""
        return 2 * (self._width + self._height)

    @property
    def width(self) -> float:
        """Return the width of the rectangle."""
        return self._width

    @property
    def height(self) -> float:
        """Return the height of the rectangle."""
        return self._height

    @property
    def type(self) -> str:
        return 'rectangle'

    @property
    def info(self) -> dict:
        """Return all info about the rectangle."""
        return {
            'type': self.type,
            'width': self.width,
            'height': self.height,
            'area': self.area,
            'perimeter': self.perimeter,
        }


class TriangleMath(IFigure):
    def __init__(self, vertices: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]):
        """
        Calculations for triangle
        :param vertices: coordinates of corners of triangle
        """
        self.__validate_input(vertices)
        self._vertices = vertices

    @staticmethod
    def __validate_input(vertices: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]):
        """Check that the given vertices are valid (for every side: a < b + c)."""
        sides = tuple(hypot(x2 - x1, y2 - y1) for (x1, y1), (x2, y2) in
                      zip(vertices, vertices[1:] + vertices[:1]))
        for side in sides:
            if side >= sum(sides) - side:
                raise ValueError("All sides must be lower to sum of other sides")

    @property
    def area(self) -> float:
        """Return the area of the triangle."""
        (x1, y1), (x2, y2), (x3, y3) = self._vertices
        return 0.5 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

    @property
    def perimeter(self) -> float:
        """Return the perimeter of the triangle."""
        return sum(self.sides)

    @property
    def vertices(self) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
        """Return all corners of the triangle considering."""
        return self._vertices

    @property
    def sides(self):
        """Return the side's lengths of the triangle."""
        return tuple(hypot(x2 - x1, y2 - y1) for (x1, y1), (x2, y2) in
                     zip(self._vertices, self._vertices[1:] + self._vertices[:1]))

    @property
    def type(self) -> str:
        return 'triangle'

    @property
    def info(self) -> dict:
        """Return all info about the triangle."""
        return {
            'type': self.type,
            'sides': self.sides,
            'area': self.area,
            'perimeter': self.perimeter,
        }
