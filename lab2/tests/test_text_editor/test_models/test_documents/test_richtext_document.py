import unittest

from text_editor.models import MarkdownDocument, MdToRichTextAdapter
from text_editor.models.text_component import TextComponent


class TestMdToRichTextAdapter(unittest.TestCase):
    def setUp(self):
        self.md_document = MarkdownDocument()
        self.adapter = MdToRichTextAdapter(self.md_document)

    def test_to_dict_includes_correct_type(self):
        result = self.adapter.to_dict()
        self.assertIn('type', result)
        self.assertEqual(result['type'], 'RichTextDocument')

    def test_users_property_is_populated_from_md_document(self):
        self.md_document._users = {"test_user": None}
        adapter = MdToRichTextAdapter(self.md_document)
        self.assertEqual(adapter.users(), self.md_document.users())

    def test_to_dict_contains_components(self):
        self.md_document._components = [TextComponent("Some text")]
        adapter = MdToRichTextAdapter(self.md_document)
        result = adapter.to_dict()
        self.assertIn('components', result)
        self.assertEqual(len(result['components']), 1)
        self.assertIn("Some text", result['components'][0]['text'])
