import unittest
from unittest.mock import MagicMock

from text_editor.models.documents.md_document import MarkdownDocument
from text_editor.models.documents.plaintext_document import MdToPlainTextAdapter


class TestMdToPlainTextAdapter(unittest.TestCase):
    def setUp(self):
        self.md_doc = MagicMock(spec=MarkdownDocument)
        self.adapter = MdToPlainTextAdapter(self.md_doc)

    def test_get_text(self):
        self.md_doc.get_text.return_value = ('# I _**can do**_ it ~~slow~~.\n'
                                             '~~work~~ correct.')
        self.assertEqual(self.adapter.get_text(), 'I can do it slow.\n'
                                                  'work correct.')


if __name__ == '__main__':
    unittest.main()
