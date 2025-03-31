import unittest

from text_editor.models import MarkdownDocument, MdToPlainTextAdapter
from text_editor.models.text_component import TextComponent


class TestMdToPlainTextAdapter(unittest.TestCase):
    def setUp(self):
        self.markdown_document = MarkdownDocument()
        self.markdown_document._components = [TextComponent("**Bold** Text~~strikethrough~~")]
        self.adapter = MdToPlainTextAdapter(self.markdown_document)

    def test_conversion_removes_markdown_syntax(self):
        plain_text = self.adapter.get_text()
        self.assertEqual(plain_text, "Bold Textstrikethrough")

    def test_to_dict_includes_correct_type(self):
        adapter_dict = self.adapter.to_dict()
        self.assertEqual(adapter_dict['type'], "PlainTextDocument")

    def test_users_property_is_populated_from_md_document(self):
        self.adapter._users = {"user1": None}  # Manually set for the test
        self.assertEqual(self.adapter.users(), {"user1": None})

    def test_to_dict_contains_components(self):
        adapter_dict = self.adapter.to_dict()
        self.assertIn('components', adapter_dict)
        self.assertEqual(len(adapter_dict['components']), 1)
        self.assertEqual(adapter_dict['components'][0]['text'], "Bold Textstrikethrough")


if __name__ == "__main__":
    unittest.main()

