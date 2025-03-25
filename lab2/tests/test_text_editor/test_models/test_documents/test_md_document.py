import unittest
from unittest.mock import MagicMock

from text_editor.models import Theme
from text_editor.models.documents.md_document import MarkdownDocument


class TestMarkdownDocument(unittest.TestCase):
    def setUp(self):
        self.document = MarkdownDocument()

    def test_apply_bold(self):
        self.document.insert_text('Some text', 0)
        self.document.apply_bold(0, 2)
        self.assertNotEqual(self.document.get_text(), 'Some text')

    def test_apply_italic(self):
        self.document.insert_text('Some text', 0)
        self.document.apply_italic(0, 2)
        self.assertNotEqual(self.document.get_text(), 'Some text')

    def test_apply_strikethrough(self):
        self.document.insert_text('Some text', 0)
        self.document.apply_strikethrough(0, 2)
        self.assertNotEqual(self.document.get_text(), 'Some text')

    def test_set_theme(self):
        mock_theme = MagicMock(spec=Theme)
        mock_theme.font_size = 2
        self.document.insert_text('Some text. \nAnd.', 0)
        self.document.set_theme(mock_theme)
        self.assertTrue(self.document.get_text().count('##') == 2)

    def test_set_theme_another_size(self):
        mock_theme = MagicMock(spec=Theme)
        mock_theme.font_size = 4
        self.document.insert_text('Some text. \nAnd.', 0)
        self.document.set_theme(mock_theme)
        self.assertTrue(self.document.get_text().count('####') == 2)


if __name__ == '__main__':
    unittest.main()
