import math

from ..interfaces import IRenderStrategy
from ..utils import RectangleMath, EllipseMath, TriangleMath


class EllipseRenderer(IRenderStrategy):
    @staticmethod
    def render(figure: EllipseMath, background: str) -> list[list[str]]:
        """Return a list of strings representing the ellipse."""
        vr = math.ceil(figure.vertical_radius)
        hr = math.ceil(figure.horizontal_radius)
        image = [[''] * (2 * hr) for _ in range(2 * vr)]

        for y in range(2 * vr):
            for x in range(2 * hr):
                dx = x - hr + 0.5
                dy = y - vr + 0.5
                if (dx ** 2) / (hr ** 2) + (dy ** 2) / (vr ** 2) <= 1:
                    image[y][x] = background
        return image


class RectangleRenderer(IRenderStrategy):
    @staticmethod
    def render(figure: RectangleMath, background: str) -> list[list[str]]:
        """Return a list of strings representing the rectangle."""
        return [[background] * int(figure.width) for _ in range(int(figure.height))]


class TriangleRenderer(IRenderStrategy):
    @staticmethod
    def render(figure: TriangleMath, background: str) -> list[list[str]]:
        """Return a list of strings representing the triangle."""
        max_x = int(max(x for x, y in figure.vertices))
        max_y = int(max(y for x, y in figure.vertices))
        image = [[''] * (max_x + 1) for _ in range(max_y + 1)]

        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if TriangleRenderer._is_point_inside(figure.area, figure.vertices, x, y):
                    image[y][x] = background
        return image

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
