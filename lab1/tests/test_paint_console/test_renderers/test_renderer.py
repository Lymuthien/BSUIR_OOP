import unittest
from unittest.mock import MagicMock
from parameterized import parameterized

from src.paint_console.renderers import BasicRenderer, ConsoleCanvasRenderer
from src.paint_console.interfaces import IDrawable


class TestBasicRenderer(unittest.TestCase):
    def setUp(self):
        self.mock_figure = MagicMock(spec=IDrawable)
        self.mock_figure.render.return_value = [['r'] * 2 for _ in range(2)]

    def test_render_successfully_updates_grid(self):
        grid = [[' '] * 4 for _ in range(4)]
        expected_grid = [
            [' '] * 4,
            [' ', 'r', 'r', ' '],
            [' ', 'r', 'r', ' '],
            [' '] * 4
        ]

        new_grid = BasicRenderer.render(self.mock_figure, 1, 1, grid)
        self.assertEqual(new_grid, expected_grid)

    @parameterized.expand([
        ("x negative", -1, 0),
        ("y negative", 0, -1),
        ("both x y negative", -1, -1),
    ])
    def test_render_x_or_y_negative_raises_error(self, test_name, x, y):
        grid = [[' '] * 4 for _ in range(4)]

        with self.subTest(msg=test_name, x=x, y=y):
            with self.assertRaisesRegex(ValueError, "x and y must be positive"):
                BasicRenderer.render(self.mock_figure, x, y, grid)

    @parameterized.expand([
        ("x out", 10, 0),
        ("y out", 0, 10),
        ("both x y out", 10, 10),
    ])
    def test_render_figure_out_of_bounds_raises_error(self, test_name, x, y):
        grid = [[' '] * 4 for _ in range(4)]

        with self.subTest(msg=test_name, x=x, y=y):
            with self.assertRaisesRegex(IndexError, "The given figure in that coordinate is out of bounds of grid."):
                BasicRenderer.render(self.mock_figure, x, y, grid)
        self.assertEqual(grid, [[' '] * 4 for _ in range(4)])

    def test_render_figure_partly_out_of_bounds_changes_grid(self):
        grid = [[' '] * 4 for _ in range(4)]

        new_grid = BasicRenderer.render(self.mock_figure, 3, 3, grid)
        self.assertEqual(new_grid, [
            [' '] * 4,
            [' '] * 4,
            [' '] * 4,
            [' ', ' ', ' ', 'r']
        ])


if __name__ == '__main__':
    unittest.main()
