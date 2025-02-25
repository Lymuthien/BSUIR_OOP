from interfaces import Figure
from math import pi, hypot, sqrt


class EllipseMath(Figure):
    def __init__(self, vertical_radius: float, horizontal_radius: float):
        self.__validate_input(vertical_radius, horizontal_radius)
        self._vertical_radius = vertical_radius
        self._horizontal_radius = horizontal_radius

    @staticmethod
    def __validate_input(vertical_radius: float, horizontal_radius: float):
        if vertical_radius < 0 or horizontal_radius < 0:
            raise ValueError("Vertical radius and horizontal radius cannot be negative")

    @property
    def area(self) -> float:
        return self._vertical_radius * self._horizontal_radius * pi

    @property
    def perimeter(self) -> float:
        return 2 * pi * sqrt((self._vertical_radius ** 2 + self._horizontal_radius ** 2) / 2)

    @property
    def vertical_radius(self) -> float:
        return self._vertical_radius

    @property
    def horizontal_radius(self) -> float:
        return self._horizontal_radius

    @property
    def type(self) -> str:
        return 'ellipse'


class RectangleMath(Figure):
    def __init__(self, width: float, height: float):
        self.__validate_input(width, height)
        self._width = width
        self._height = height

    @staticmethod
    def __validate_input(width: float, height: float):
        if width < 0 or height < 0:
            raise ValueError("Width and height cannot be negative")

    @property
    def area(self) -> float:
        return self._width * self._height

    @property
    def perimeter(self) -> float:
        return 2 * (self._width + self._height)

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def type(self) -> str:
        return 'rectangle'


class TriangleMath(Figure):
    def __init__(self, vertices: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]):
        self.__validate_input(vertices)
        self._vertices = vertices

    @staticmethod
    def __validate_input(vertices: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]):
        sides = tuple(hypot(x2 - x1, y2 - y1) for (x1, y1), (x2, y2) in
                      zip(vertices, vertices[1:] + vertices[:1]))
        for side in sides:
            if side >= sum(sides) - side:
                raise ValueError("All sides must be greater than or equal to sum of sides")

    @property
    def area(self) -> float:
        (x1, y1), (x2, y2), (x3, y3) = self._vertices
        return 0.5 * abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))

    @property
    def perimeter(self) -> float:
        return sum(hypot(x2 - x1, y2 - y1) for (x1, y1), (x2, y2) in
                   zip(self._vertices, self._vertices[1:] + self._vertices[:1]))

    @property
    def vertices(self) -> tuple[tuple[float, float], ...]:
        return self._vertices

    @property
    def type(self) -> str:
        return 'triangle'
