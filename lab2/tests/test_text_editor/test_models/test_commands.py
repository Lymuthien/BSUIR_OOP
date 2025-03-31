import unittest
from unittest.mock import MagicMock

from text_editor.interfaces import IDocument
from text_editor.models import WriteCommand, EraseCommand, ChangeStyleCommand, Theme, ChangeThemeCommand, \
    MarkdownDocument


class TestWriteCommand(unittest.TestCase):
    def setUp(self):
        self.mock_document = MagicMock(spec=IDocument)
        self.text = 'text'
        self.pos = 0
        self.write_command = WriteCommand(self.text, self.pos, self.mock_document)

    def test_execute(self):
        self.write_command.execute()
        self.mock_document.insert_text.assert_called_once_with(self.text, self.pos)

    def test_undo(self):
        self.write_command.undo()
        self.mock_document.delete_text.assert_called_once_with(self.pos, self.pos + len(self.text) - 1)


class TestEraseCommand(unittest.TestCase):
    def setUp(self):
        self.mock_document = MagicMock(spec=IDocument)
        self.start = 0
        self.end = 1
        self.erase_command = EraseCommand(self.start, self.end, self.mock_document)

    def test_execute(self):
        self.erase_command.execute()
        self.mock_document.delete_text.assert_called_once_with(self.start, self.end)

    def test_undo(self):
        self.erase_command.undo()
        self.mock_document.insert_text.assert_called_once()


class TestChangeStyleCommand(unittest.TestCase):
    def setUp(self):
        self.mock_document = MagicMock(spec=MarkdownDocument)
        self.mock_document.apply_bold = MagicMock()
        self.mock_document.apply_italic = MagicMock()
        self.mock_document.apply_strikethrough = MagicMock()
        self.mock_document.get_text.return_value = 'text'

        self.command = ChangeStyleCommand(0, 1, self.mock_document, True, True, True)

    def test_execute(self):
        self.command.execute()
        self.mock_document.apply_bold.assert_called_once_with(0, 1)
        self.mock_document.apply_italic.assert_called_once_with(0, 1)
        self.mock_document.apply_strikethrough.assert_called_once_with(0, 1)

    def test_undo(self):
        self.command.execute()
        self.command.undo()
        self.mock_document.replace_text.assert_called_once()


class TestChangeThemeCommand(unittest.TestCase):
    def setUp(self):
        self.mock_document = MagicMock(spec=IDocument)
        self.mock_document.get_text.return_value = 'text'
        self.mock_theme = MagicMock(spec=Theme)

        self.command = ChangeThemeCommand(self.mock_document, self.mock_theme)

    def test_execute(self):
        self.command.execute()
        self.mock_document.set_theme.assert_called_once_with(self.mock_theme)

    def test_undo(self):
        self.command.execute()
        self.command.undo()
        self.mock_document.replace_text.assert_called_once()


if __name__ == '__main__':
    unittest.main()
