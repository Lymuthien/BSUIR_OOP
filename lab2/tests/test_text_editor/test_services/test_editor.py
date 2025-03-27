import unittest
from unittest.mock import MagicMock

from text_editor.interfaces import IFileManager, ISerializer
from text_editor.services import Editor, EditorSettings


class TestEditor(unittest.TestCase):
    def setUp(self):
        self.mock_loader = MagicMock(spec=IFileManager)
        self.mock_serializer = MagicMock(spec=ISerializer)
        self.editor = Editor({'l': self.mock_loader}, {'s': self.mock_serializer})

    def test_settings(self):
        self.assertEqual(self.editor.settings, EditorSettings())

    def test_create_document(self):
        self.assertTrue(isinstance(self.editor.create_document(), str))

    def test_is_opened(self):
        self.assertFalse(self.editor.is_opened())

    def test_is_opened_after_creation(self):
        self.editor.create_document()
        self.assertTrue(self.editor.is_opened)

    def test_open_document(self):
        self.editor.open_document('lalala.s', 'l')
        self.mock_loader.load.assert_called_once()

    def test_open_document_incorrect_ext(self):
        with self.assertRaises(Exception):
            self.editor.open_document('lalala.incorrect', 'l')

    def test_open_document_unknown_loader(self):
        with self.assertRaises(Exception):
            self.editor.open_document('lalala.l', 'unknown')

    def test_close_document(self):
        self.editor.open_document('lalala.s', 'l')
        self.editor.close_document()
        self.assertFalse(self.editor.is_opened())

    def test_insert_text(self):
        self.editor.create_document()
        self.editor.insert_text('text', 0)
        self.assertEqual(self.editor.get_text(), 'text')

    def test_undo(self):
        self.editor.create_document()
        self.editor.insert_text('text', 0)
        self.editor.undo()
        self.assertEqual(self.editor.get_text(), '')

    def test_redo(self):
        self.editor.create_document()
        self.editor.insert_text('text', 0)
        self.editor.undo()
        self.editor.redo()
        self.assertEqual(self.editor.get_text(), 'text')

    def test_erase_text(self):
        self.editor.create_document()
        self.editor.insert_text('text', 0)
        self.editor.erase_text(0, 1)
        self.assertEqual(self.editor.get_text(), 'xt')



if __name__ == '__main__':
    unittest.main()
