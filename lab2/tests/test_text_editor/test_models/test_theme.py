import unittest

from text_editor.models import Theme


class TestTheme(unittest.TestCase):
    def setUp(self):
        self.theme = Theme(11, False, True)

    def test_font_size(self):
        self.assertEqual(self.theme.font_size, 11)

    def test_italic(self):
        self.assertEqual(self.theme.italic, False)

    def test_bold(self):
        self.assertEqual(self.theme.bold, True)


if __name__ == '__main__':
    unittest.main()
