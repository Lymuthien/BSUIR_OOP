import unittest

from text_editor.models import EditorSettings


class TestEditorSettings(unittest.TestCase):
    def setUp(self):
        self.settings = EditorSettings()
        self.other_settings = EditorSettings()

    def test_singleton(self):
        self.assertEqual(self.settings, self.other_settings)

    def test_font_size(self):
        self.assertEqual(self.settings.font_size, 11)

    def test_font_size_setter(self):
        self.settings.font_size = 12
        self.assertEqual(self.settings.font_size, 12)

    def test_singleton_font_size(self):
        self.settings.font_size = 13
        self.assertEqual(self.other_settings.font_size, 13)


if __name__ == '__main__':
    unittest.main()
