import unittest
from unittest.mock import MagicMock

from paint_console.core import AddFigureCommand, RemoveFigureCommand, MoveFigureCommand, ChangeFigureBgCommand
from paint_console.interfaces import ICommand, ICanvasModel, ICanvasView, IDrawable


class TestAddFigureCommand(unittest.TestCase):
    def setUp(self):
        self.mock_command = MagicMock(spec=ICommand)
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


if __name__ == '__main__':
    unittest.main()
