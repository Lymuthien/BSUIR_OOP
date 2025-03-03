import unittest
from unittest.mock import MagicMock

from paint_console.core import AddFigureCommand, RemoveFigureCommand, MoveFigureCommand, ChangeFigureBgCommand
from paint_console.interfaces import ICanvasModel, ICanvasView, IDrawable, ISearchingCanvasModel


class TestAddFigureCommand(unittest.TestCase):
    def setUp(self):
        self.mock_view = MagicMock(spec=ICanvasView)
        self.mock_model = MagicMock(spec=ICanvasModel)
        self.mock_figure = MagicMock(spec=IDrawable)

        self.layer = self.mock_model.new_layer.return_value = 5
        self.figure_id = self.mock_model.add_figure.return_value = 'figure_id'
        self.mock_model.get_figure_layout.return_value.layer = self.layer

        self.x = 10
        self.y = 20

    def test_add_figure_init_executes_commands(self):
        AddFigureCommand(self.mock_model, self.mock_view, self.mock_figure, self.x, self.y)
        self.mock_model.add_figure.assert_called_once_with(
            self.mock_figure, self.x, self.y, layer=self.layer
        )
        self.mock_model.get_figure_layout.assert_called_once_with(self.figure_id)
        self.mock_view.draw_figure.assert_called_once_with(
            self.mock_figure, self.x, self.y
        )

    def test_undo_removes_figure(self):
        command = AddFigureCommand(self.mock_model, self.mock_view, self.mock_figure, 0, 0)
        command.undo()
        self.mock_model.remove_figure.assert_called_once_with(self.figure_id)
        self.mock_view.update.assert_called_once()

    def test_redo_restores_figure(self):
        command = AddFigureCommand(self.mock_model, self.mock_view, self.mock_figure, self.x, self.y)
        command.undo()
        command.redo()
        self.mock_model.add_figure.assert_called_with(
            self.mock_figure, self.x, self.y, layer=self.layer, figure_id=self.figure_id
        )
        self.assertEqual(self.mock_view.update.call_count, 2)


class TestRemoveFigureCommand(unittest.TestCase):
    def setUp(self):
        self.mock_view = MagicMock(spec=ICanvasView)
        self.mock_model = MagicMock(spec=ISearchingCanvasModel)
        self.mock_figure = MagicMock(spec=IDrawable)

        self.figure_id = self.mock_model.search.return_value = 'figure_id'
        self.mock_model.get_figure_layout.return_value.layer = self.layer = 1
        self.mock_model.get_figure_layout.return_value.coordinates = self.coordinates = 1, 4

    def test_remove_figure_init_executes_commands(self):
        RemoveFigureCommand(self.mock_model, self.mock_view, self.mock_figure)
        self.mock_model.get_figure_layout.assert_called_with(self.figure_id)
        self.mock_model.remove_figure.assert_called_once_with(self.figure_id)
        self.mock_view.update.assert_called_once()

    def test_undo_adds_figure(self):
        command = RemoveFigureCommand(self.mock_model, self.mock_view, self.mock_figure)
        command.undo()
        self.mock_model.add_figure.assert_called_once_with(self.mock_figure, *self.coordinates,
                                                           layer=self.layer, figure_id=self.figure_id)
        self.assertEqual(self.mock_view.update.call_count, 2)

    def test_redo_removes_figure(self):
        command = RemoveFigureCommand(self.mock_model, self.mock_view, self.mock_figure)
        command.undo()
        command.redo()
        self.assertEqual(self.mock_model.remove_figure.call_count, 2)
        self.assertEqual(self.mock_view.update.call_count, 3)


class TestMoveFigureCommand(unittest.TestCase):
    def setUp(self):
        self.mock_view = MagicMock(spec=ICanvasView)
        self.mock_model = MagicMock(spec=ISearchingCanvasModel)
        self.mock_figure = MagicMock(spec=IDrawable)

        self.new_coordinates = 4, 8
        self.figure_id = self.mock_model.search.return_value = 'figure_id'
        self.mock_model.get_figure_layout.return_value.coordinates = self.old_coordinates = 1, 4

    def test_move_figure_init_executes_command(self):
        MoveFigureCommand(self.mock_model, self.mock_view, self.mock_figure, *self.new_coordinates)

        self.mock_model.search.assert_called_once_with(self.mock_figure)
        self.mock_model.get_figure_layout.assert_called_with(self.figure_id)

        layout = self.mock_model.get_figure_layout.return_value
        self.assertEqual(layout.coordinates, self.new_coordinates)
        self.mock_view.update.assert_called_once()

    def test_undo_behavior(self):
        command = MoveFigureCommand(self.mock_model, self.mock_view, self.mock_figure, *self.new_coordinates)
        command.undo()

        layout = self.mock_model.get_figure_layout.return_value
        self.assertEqual(layout.coordinates, self.old_coordinates)
        self.assertEqual(self.mock_view.update.call_count, 2)

    def test_redo_behavior(self):
        command = MoveFigureCommand(self.mock_model, self.mock_view, self.mock_figure, *self.new_coordinates)
        command.undo()
        command.redo()

        layout = self.mock_model.get_figure_layout.return_value
        self.assertEqual(layout.coordinates, self.new_coordinates)
        self.assertEqual(self.mock_view.update.call_count, 3)

    def test_multiple_undo_redo_cycles(self):
        command = MoveFigureCommand(self.mock_model, self.mock_view, self.mock_figure, *self.new_coordinates)

        for _ in range(3):
            command.undo()
            command.redo()

        layout = self.mock_model.get_figure_layout.return_value
        self.assertEqual(layout.coordinates, self.new_coordinates)


class TestChangeFigureBgCommand(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock(spec=ISearchingCanvasModel)
        self.mock_view = MagicMock(spec=ICanvasView)
        self.mock_figure = MagicMock(spec=IDrawable)

        self.new_bg = '+'

        self.mock_model.search.return_value = self.figure_id = 'figure_id'
        self.mock_layout = MagicMock()
        self.mock_layout.figure.background = self.old_bg = '*'
        self.mock_model.get_figure_layout.return_value = self.mock_layout

    def test_change_figure_bg_executes_commands(self):
        ChangeFigureBgCommand(self.mock_model, self.mock_view, self.mock_figure, self.new_bg)

        self.mock_model.get_figure_layout.assert_called_with(self.figure_id)
        self.mock_model.search.assert_called_once_with(self.mock_figure)

        self.assertEqual(self.mock_layout.figure.background, self.new_bg)
        self.mock_view.update.assert_called_once()

    def test_undo_behavior(self):
        command = ChangeFigureBgCommand(self.mock_model, self.mock_view, self.mock_figure, self.new_bg)

        command.undo()

        self.assertEqual(self.mock_layout.figure.background, self.old_bg)
        self.assertEqual(self.mock_view.update.call_count, 2)

    def test_redo_behavior(self):
        command = ChangeFigureBgCommand(self.mock_model, self.mock_view, self.mock_figure, self.new_bg)
        command.undo()
        command.redo()

        self.assertEqual(self.mock_layout.figure.background, self.new_bg)
        self.assertEqual(self.mock_view.update.call_count, 3)

    def test_multiple_undo_redo_cycles(self):
        command = ChangeFigureBgCommand(self.mock_model, self.mock_view, self.mock_figure, self.new_bg)

        for _ in range(3):
            command.undo()
            command.redo()

        self.assertEqual(self.mock_layout.figure.background, self.new_bg)


if __name__ == '__main__':
    unittest.main()
