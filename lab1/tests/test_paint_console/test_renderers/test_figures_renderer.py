import unittest
from unittest.mock import MagicMock

from paint_console.renderers import EllipseRenderer, RectangleRenderer, TriangleRenderer
from paint_console.utils import EllipseMath, RectangleMath, TriangleMath


class TestEllipseRenderer(unittest.TestCase):
    def setUp(self):
        self.mock_figure = MagicMock(spec=EllipseMath)
        self.vr = self.mock_figure.vertical_radius = 2
        self.hr = self.mock_figure.horizontal_radius = 4
        self.background = '*'

    def test_render_grid_sizes_match(self):
        grid = EllipseRenderer.render(self.mock_figure, self.background)

        self.assertEqual(len(grid), 2 * self.vr)
        self.assertEqual(len(grid[0]), 2 * self.hr)

    def test_render_grid_image_match(self):
        grid = EllipseRenderer.render(self.mock_figure, self.background)

        for y in range(2 * self.vr):
            for x in range(2 * self.hr):
                dx = x - self.hr + 0.5
                dy = y - self.vr + 0.5
                if (dx ** 2) / (self.hr ** 2) + (dy ** 2) / (self.vr ** 2) <= 1:
                    self.assertEqual(grid[y][x], self.background)
                else:
                    self.assertEqual(grid[y][x], '')


class TestRectangleRenderer(unittest.TestCase):
    def setUp(self):
        self.mock_figure = MagicMock(spec=RectangleMath)
        self.width = self.mock_figure.width = 2
        self.height = self.mock_figure.height = 4
        self.background = '*'

    def test_render_grid_sizes_match(self):
        grid = RectangleRenderer.render(self.mock_figure, self.background)

        self.assertEqual(len(grid), self.height)
        self.assertEqual(len(grid[0]), self.width)

    def test_render_grid_image_match(self):
        grid = RectangleRenderer.render(self.mock_figure, self.background)

        self.assertListEqual(grid, [['*'] * self.width for _ in range(self.height)])


class TestTriangleRenderer(unittest.TestCase):
    def setUp(self):
        self.mock_figure = MagicMock(spec=TriangleMath)
        self.vertices = self.mock_figure.vertices = ((0, 0), (0, 3), (4, 0))
        self.background = '*'
        self.mock_figure.area = 6

    def test_render_grid_sizes_match(self):
        grid = TriangleRenderer.render(self.mock_figure, self.background)

        self.assertEqual(len(grid), 4)
        self.assertEqual(len(grid[0]), 5)


if __name__ == '__main__':
    unittest.main()
