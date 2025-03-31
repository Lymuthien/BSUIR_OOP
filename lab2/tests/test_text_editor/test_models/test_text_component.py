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
        self.text_component = TextComponent("Sample text")
        self.bold_text_component = BoldTextComponent(self.text_component)

    def test_get_text_applies_bold_formatting(self):
        # Arrange
        input_text = "This is a line"
        text_component = TextComponent(input_text)
        bold_text = BoldTextComponent(text_component)

        # Act
        result = bold_text.get_text()

        # Assert
        self.assertEqual(result, "**This is a line**")

    def test_get_text_skips_lines_with_only_asterisks(self):
        # Arrange
        input_text = "***"
        text_component = TextComponent(input_text)
        bold_text = BoldTextComponent(text_component)

        # Act
        result = bold_text.get_text()

        # Assert
        self.assertEqual(result, "***")

    def test_get_text_handles_multiline_text(self):
        # Arrange
        input_text = "Line 1\nLine 2\n***\nLine 3"
        text_component = TextComponent(input_text)
        bold_text = BoldTextComponent(text_component)

        # Act
        result = bold_text.get_text()

        # Assert
        expected_output = "**Line 1**\n**Line 2**\n***\n**Line 3**"
        self.assertEqual(result, expected_output)

    def test_to_dict_returns_correct_representation(self):
        # Act
        result = self.bold_text_component.to_dict()

        # Assert
        self.assertEqual(result["type"], "BoldTextComponent")
        self.assertEqual(result["text"], "**Sample text**")

    def test_from_dict_restores_from_data(self):
        # Arrange
        input_data = {"type": "BoldTextComponent", "text": "Restored text"}

        # Act
        restored_component = BoldTextComponent().from_dict(input_data)

        # Assert
        self.assertEqual(restored_component.get_text(), "**Restored text**")


class TestItalicTextComponent(unittest.TestCase):
    def setUp(self):
        self.text = 'some text'
        self.text_component = TextComponent(self.text)
        self.italic_component = ItalicTextComponent(self.text_component)

    def text_get_text(self):
        self.assertEqual(self.italic_component.get_text(),
                         f'*{self.text_component.get_text()}*')

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
                         f'~{self.text_component.get_text()}~')

    def test_get_text_not_bold_empty(self):
        text_component = TextComponent('')
        strikethrough_component = StrikethroughTextComponent(text_component)

        self.assertEqual(strikethrough_component.get_text(), '')


if __name__ == '__main__':
    unittest.main()
