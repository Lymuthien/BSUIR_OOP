import unittest

from text_editor.factories.document_factory import MDFactory, RichTextFactory, PlainTextFactory
from text_editor.models import RichTextDocument, PlainTextDocument, MarkdownDocument


class TestMDFactory(unittest.TestCase):
    def setUp(self):
        self.factory = MDFactory()

    def test_create_document_returns_markdown_document(self):
        document = self.factory.create_document()
        self.assertIsInstance(document, MarkdownDocument)


class TestRichTextFactory(unittest.TestCase):
    def setUp(self):
        self.factory = RichTextFactory()

    def test_create_document_returns_richtext_document(self):
        document = self.factory.create_document()
        self.assertIsInstance(document, RichTextDocument)


class TestPlainTextFactory(unittest.TestCase):
    def setUp(self):
        self.factory = PlainTextFactory()

    def test_create_document_returns_plaintext_document(self):
        document = self.factory.create_document()
        self.assertIsInstance(document, PlainTextDocument)


if __name__ == "__main__":
    unittest.main()
