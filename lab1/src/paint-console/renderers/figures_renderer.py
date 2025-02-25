from interfaces import RenderStrategy
from mathematics import *


class EllipseRenderer(RenderStrategy):
    def render(self, figure: EllipseMath, background: str) -> list[list[str]]:
        vr = int(figure.vertical_radius)
        hr = int(figure.horizontal_radius)
        image = [[''] * (2 * hr) for _ in range(2 * vr)]

        for y in range(2 * vr):
            for x in range(2 * hr):
                dx = x - hr
                dy = y - vr
                if (dx ** 2) / (hr ** 2) + (dy ** 2) / (vr ** 2) <= 1:
                    image[y][x] = background
        return image


class RectangleRenderer(RenderStrategy):
    def render(self, figure: RectangleMath, background: str) -> list[list[str]]:
        return [[background] * int(figure.width) for _ in range(int(figure.height))]


class TriangleRenderer(RenderStrategy):
    def render(self, figure: TriangleMath, background: str) -> list[list[str]]:
        max_x = int(max(x for x, y in figure.vertices))
        max_y = int(max(y for x, y in figure.vertices))
        image = [[''] * (max_x + 1) for _ in range(max_y + 1)]

        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if self._is_point_inside(figure.vertices, x, y):
                    image[y][x] = background
        return image

    def _is_point_inside(self, vertices, x, y):
        pass
