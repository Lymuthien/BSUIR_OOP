import unittest

from text_editor.models.text_component import TextComponent, BoldTextComponent, ItalicTextComponent, \
    StrikethroughTextComponent


class TestTextComponent(unittest.TestCase):
    def setUp(self):
        self.text = 'some text'
        self.text_component = TextComponent(self.text)

    def test_get_text(self):
        self.assertEqual(self.text_component.get_text(), self.text)


class TestBoldTextComponent(unittest.TestCase):
    def setUp(self):
        self.text = 'some text'
        self.text_component = TextComponent(self.text)
        self.bold_component = BoldTextComponent(self.text_component)

    def text_get_text(self):
        self.assertEqual(self.bold_component.get_text(),
                         f'**{self.text_component.get_text()}**')

    def test_get_text_not_bold_empty(self):
        text_component = TextComponent('')
        bold_component = BoldTextComponent(text_component)

        self.assertEqual(bold_component.get_text(), '')


class TestItalicTextComponent(unittest.TestCase):
    def setUp(self):
        self.text = 'some text'
        self.text_component = TextComponent(self.text)
        self.italic_component = ItalicTextComponent(self.text_component)

    def text_get_text(self):
        self.assertEqual(self.italic_component.get_text(),
                         f'_{self.text_component.get_text()}_')

    def test_get_text_not_bold_empty(self):
        text_component = TextComponent('')
        italic_component = ItalicTextComponent(text_component)

        self.assertEqual(italic_component.get_text(), '')


class TestStrikethroughTextComponent(unittest.TestCase):
    def setUp(self):
        self.text = 'some text'
        self.text_component = TextComponent(self.text)
        self.strikethrough_component = StrikethroughTextComponent(self.text_component)

    def text_get_text(self):
        self.assertEqual(self.strikethrough_component.get_text(),
                         f'_{self.text_component.get_text()}_')

    def test_get_text_not_bold_empty(self):
        text_component = TextComponent('')
        strikethrough_component = StrikethroughTextComponent(text_component)

        self.assertEqual(strikethrough_component.get_text(), '')


if __name__ == '__main__':
    unittest.main()
