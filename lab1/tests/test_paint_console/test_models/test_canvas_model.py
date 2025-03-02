import unittest
from unittest.mock import MagicMock, patch, PropertyMock

# from ....src.paint_console.models import FigureLayout, CanvasModel, CanvasView
# from ....src.paint_console.interfaces import IDrawable
from src.paint_console.models import FigureLayout, CanvasModel, CanvasView
from src.paint_console.interfaces import IDrawable, ICanvasModel, IRenderer


class TestFigureLayout(unittest.TestCase):
    def setUp(self):
        self.mock_figure = MagicMock(spec=IDrawable)

    def test_figure_layout_init_negative_layer_raises_exception(self):
        with self.assertRaises(ValueError):
            FigureLayout(self.mock_figure, (0, 0), -1)

    def test_figure_layout_init_zero_layer_not_raises_exception(self):
        FigureLayout(self.mock_figure, (0, 0), 0)

    def test_figure_layout_init_properties_match(self):
        for i in range(3):
            figure_layout = FigureLayout(self.mock_figure, (i, i), i)
            self.assertEqual(figure_layout.figure, self.mock_figure)
            self.assertTupleEqual(figure_layout.coordinates, (i, i))
            self.assertEqual(figure_layout.layer, i)

    def test_coordinates_setter_match(self):
        figure_layout = FigureLayout(self.mock_figure, (0, 0), 0)
        figure_layout.coordinates = (100, 200)
        self.assertTupleEqual(figure_layout.coordinates, (100, 200))

    def test_info_returns_matching_dict(self):
        figure_layout = FigureLayout(self.mock_figure, (0, 0), 0)

        self.mock_figure.info = {
            'type': 'rectangle',
            'background': '+'
        }

        expected_result = {
            'type': 'rectangle',
            'background': '+',
            'coordinates': (0, 0),
            'layer': 0
        }

        result = figure_layout.info
        self.assertDictEqual(result, expected_result)


class TestCanvasModel(unittest.TestCase):
    pass


class TestCanvasView(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock(spec=ICanvasModel)
        self.mock_renderer = MagicMock(spec=IRenderer)
        self.width = 10
        self.height = 3
        self.mock_renderer.render.return_value = [['*'] * self.width for _ in range(self.height)]

        self.canvas = CanvasView(self.mock_model, self.mock_renderer, width=self.width, height=self.height)

    def test_init_all_properties_match(self):
        self.assertEqual(self.canvas.width, self.width)
        self.assertEqual(self.canvas.height, self.height)
        self.assertEqual(len(self.canvas.grid), self.height)
        self.assertEqual(len(self.canvas.grid[0]), self.width)
        self.assertTrue(all(cell == ' ' for row in self.canvas.grid for cell in row))

    def test_draw_figure_changes_grid(self):
        mock_figure = MagicMock(spec=IDrawable)
        self.canvas.draw_figure(mock_figure, 10, 5)

        self.assertTupleEqual(self.canvas.grid, tuple(tuple('*') * self.width for _ in range(self.height)))

    def test_clear_resets_grid(self):
        self.canvas = CanvasView(self.mock_model, self.mock_renderer, width=self.width, height=self.height)
        mock_figure = MagicMock(spec=IDrawable)
        self.canvas.draw_figure(mock_figure, 10, 5)
        self.canvas.clear()

        self.assertTrue(all(cell == ' ' for row in self.canvas.grid for cell in row))


if __name__ == '__main__':
    unittest.main()
