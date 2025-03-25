import unittest
from unittest.mock import MagicMock

from text_editor.models.documents.md_document import MarkdownDocument
from text_editor.models.documents.richtext_document import MdToRichTextAdapter


class TestMdRichTextAdapter(unittest.TestCase):
    def setUp(self):
        self.mock_doc = MagicMock(spec=MarkdownDocument)
        self.adapter = MdToRichTextAdapter(self.mock_doc)

    def test_get_text(self):
        self.mock_doc.get_text.return_value = '## Show me **your** homework.\n'
        self.assertEqual(self.adapter.get_text(),
                         '{\\rtf1 \\pard \\ql \\f0 \\sa180 \\li0 \\fi0 \\outlinelevel1 \\b \\fs32 Show '
                         'me {\\b your} homework.\\par}\r\n')


if __name__ == '__main__':
    unittest.main()
