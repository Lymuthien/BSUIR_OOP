from interfaces import IRenderStrategy
from mathematics import RectangleMath, EllipseMath, TriangleMath


class EllipseRenderer(IRenderStrategy):
    @staticmethod
    def render(figure: EllipseMath, background: str) -> list[list[str]]:
        vr = int(figure.vertical_radius)
        hr = int(figure.horizontal_radius)
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
        return [[background] * int(figure.width) for _ in range(int(figure.height))]


class TriangleRenderer(IRenderStrategy):
    def render(self, figure: TriangleMath, background: str) -> list[list[str]]:
        max_x = int(max(x for x, y in figure.vertices))
        max_y = int(max(y for x, y in figure.vertices))
        image = [[''] * (max_x + 1) for _ in range(max_y + 1)]

        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if self._is_point_inside(figure.area, figure.vertices, x, y):
                    image[y][x] = background
        return image

    @staticmethod
    def _is_point_inside(basic_area, vertices, x, y) -> bool:
        """If areas of all triangles in sum gives basic area, point inside it."""
        try:
            a, b, c = vertices
            triangles = [TriangleMath((a, b, (x, y))),
                         TriangleMath((a, c, (x, y))),
                         TriangleMath((b, c, (x, y)))]

            triangle_areas = map(lambda triangle: triangle.area, triangles)
            if sum(triangle_areas) - basic_area < 1:
                return True
            return False
        except ValueError:
            return False
