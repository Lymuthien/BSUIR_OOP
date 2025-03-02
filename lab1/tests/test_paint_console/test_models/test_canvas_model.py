import unittest
from unittest.mock import MagicMock, patch, PropertyMock

# from ....src.paint_console.models import FigureLayout, CanvasModel, CanvasView
# from ....src.paint_console.interfaces import IDrawable
from src.paint_console.models import FigureLayout, CanvasModel, CanvasView
from src.paint_console.interfaces import IDrawable, ICanvasModel, IRenderer, INavigator


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
    def setUp(self):
        self.mock_navigator = MagicMock(spec=INavigator)
        self.mock_figure = MagicMock(spec=IDrawable)
        self.layout = MagicMock(spec=FigureLayout)
        self.layout.figure = self.mock_figure
        self.model = CanvasModel(navigator=self.mock_navigator)

    def test_add_figure_generates_uuid(self):
        figure_id = self.model.add_figure(self.mock_figure, 0, 0)
        self.assertIsInstance(figure_id, str)
        self.assertIn(figure_id, self.model.get_data)

    def test_add_figure_with_id_returns_id(self):
        figure_id = self.model.add_figure(self.mock_figure, 0, 0, figure_id='custom_id')
        self.assertIsInstance(figure_id, str)
        self.assertIn(figure_id, self.model.get_data)

    def test_add_figure_calls_navigator(self):
        self.model.add_figure(self.mock_figure, 10, 20, 5)
        self.mock_navigator.append.assert_called_once_with(self.mock_figure)

    def test_remove_figure_with_non_existing_figure_id_raises_exception(self):
        with self.assertRaises(KeyError):
            self.model.remove_figure('random_id')

    def test_remove_figure_figure_not_in_store(self):
        figure_id = self.model.add_figure(self.mock_figure, 0, 0)
        self.model.remove_figure(figure_id)

        self.assertNotIn(figure_id, self.model.get_data)
        self.mock_navigator.remove.assert_called_once_with(self.mock_figure)

    def test_new_layer_empty_list_returns_zero(self):
        self.model.load_data({})
        self.assertEqual(self.model.new_layer(), 0)

    def test_new_layer_after_adding_figure_returns_next(self):
        self.model.load_data({})
        self.model.add_figure(self.mock_figure, 0, 0)
        self.assertEqual(self.model.new_layer(), 1)
        self.model.add_figure(self.mock_figure, 10, 20, layer=1)
        self.assertEqual(self.model.new_layer(), 2)
        self.model.add_figure(self.mock_figure, 10, 20, layer=10)
        self.assertEqual(self.model.new_layer(), 11)

    def test_load_data(self):
        test_data = {'test_id': self.layout}

        self.model.load_data(test_data)
        self.mock_navigator.append.assert_called_with(self.mock_figure)
        self.assertEqual(self.model.get_data, test_data)

    def test_get_figure_layout(self):
        test_data = {'test_id': self.layout}

        self.model.load_data(test_data)
        self.assertEqual(self.model.get_figure_layout('test_id'), self.layout)

    def test_get_figure_layout_with_non_existing_index_raises_error(self):
        self.model.load_data({})
        with self.assertRaises(KeyError):
            self.model.get_figure_layout('example_id')

    def test_search_success_return_id(self):
        self.model.load_data({})
        figure_id = self.model.add_figure(self.mock_figure, 0, 0)
        self.assertEqual(self.model.search(self.mock_figure), figure_id)

    def test_search_with_same_object_return_first_id_without_start(self):
        self.model.load_data({})
        figure_id = self.model.add_figure(self.mock_figure, 0, 0)
        self.model.add_figure(self.mock_figure, 0, 0)
        self.model.add_figure(self.mock_figure, 0, 0)
        self.assertEqual(self.model.search(self.mock_figure), figure_id)

    def test_search_with_same_object_return_id_from_start_index(self):
        self.model.load_data({})

        figure_id = 0
        for _ in range(3):
            figure_id = self.model.add_figure(self.mock_figure, 0, 0)
        self.assertEqual(self.model.search(self.mock_figure, 2), figure_id)

    def test_search_non_existing_object_returns_none(self):
        self.model.load_data({})

        self.assertEqual(self.model.search(self.mock_figure), None)



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
