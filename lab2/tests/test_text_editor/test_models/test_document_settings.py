import unittest
from unittest.mock import MagicMock

from text_editor.models import Theme
from text_editor.models.document_settings import DocumentSettings


class TestDocumentSettings(unittest.TestCase):
    def setUp(self):
        self.settings = DocumentSettings()

    def test_read_only(self):
        self.assertEqual(self.settings.read_only, False)

    def test_read_only_setter(self):
        self.settings.read_only = True
        self.assertEqual(self.settings.read_only, True)

    def test_hash_password(self):
        self.assertEqual(self.settings.hash_password, None)

    def test_hash_password_setter(self):
        self.settings.hash_password = '<PASSWORD>'
        self.assertEqual(self.settings.hash_password, '<PASSWORD>')

    def test_font_size(self):
        self.assertEqual(self.settings.font_size, 4)

    def test_font_size_setter(self):
        self.settings.font_size = 1
        self.assertEqual(self.settings.font_size, 1)

    def test_all_bold(self):
        self.assertEqual(self.settings.all_bold, False)

    def test_all_bold_setter(self):
        self.settings.all_bold = True
        self.assertEqual(self.settings.all_bold, True)

    def test_all_italic(self):
        self.assertEqual(self.settings.all_italic, False)

    def test_all_italic_setter(self):
        self.settings.all_italic = True
        self.assertEqual(self.settings.all_italic, True)

    def test_set_theme(self):
        mock_theme = MagicMock(spec=Theme)
        mock_theme.font_size = 1
        mock_theme.bold = True
        mock_theme.italic = True

        self.settings.set_theme(mock_theme)
        self.assertEqual(self.settings.font_size, mock_theme.font_size)
        self.assertEqual(self.settings.all_bold, mock_theme.bold)
        self.assertEqual(self.settings.all_italic, mock_theme.italic)

if __name__ == '__main__':
    unittest.main()
