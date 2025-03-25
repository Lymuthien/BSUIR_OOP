import unittest
from unittest.mock import MagicMock

from text_editor.services import HistoryManager
from text_editor.interfaces import ICommand


class TestHistoryManager(unittest.TestCase):
    def setUp(self):
        self.mock_command = MagicMock(spec=ICommand)

    def test_add_command_success(self):
        history = HistoryManager()
        history.add_command(self.mock_command)

    def test_add_command_redo_stack_clears(self):
        history = HistoryManager()
        history.add_command(self.mock_command)
        history.undo()
        history.add_command(self.mock_command)
        with self.assertRaises(IndexError):
            history.redo()

    def test_undo_with_empty_stack_raises_exception(self):
        history = HistoryManager()
        with self.assertRaises(IndexError):
            history.undo()

    def test_undo_with_not_empty_than_redo(self):
        history = HistoryManager()
        history.add_command(self.mock_command)
        history.undo()
        history.redo()

    def test_undo_with_few_commands(self):
        history = HistoryManager()
        for _ in range(3):
            history.add_command(self.mock_command)
        for _ in range(3):
            history.undo()

    def test_redo_with_empty_stack_raises_exception(self):
        history = HistoryManager()
        with self.assertRaises(IndexError):
            history.redo()

    def test_redo_than_undo(self):
        history = HistoryManager()
        history.add_command(self.mock_command)
        history.undo()
        history.redo()
        history.undo()


if __name__ == '__main__':
    unittest.main()
