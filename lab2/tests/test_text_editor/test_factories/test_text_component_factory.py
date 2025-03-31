import unittest

from text_editor.factories.text_component_factory import BasicTextComponentFactory, BoldTextComponentFactory, \
    ItalicTextComponentFactory, StrikethroughTextComponentFactory
from text_editor.interfaces.itext_component import ITextComponent
from text_editor.models.text_component import TextComponent, BoldTextComponent, ItalicTextComponent, \
    StrikethroughTextComponent


class TestBasicTextComponentFactory(unittest.TestCase):
    def setUp(self):
        self.factory = BasicTextComponentFactory()

    def test_create_text_component_returns_text_component_instance(self):
        component = self.factory.create_text_component()
        self.assertIsInstance(component, TextComponent)

    def test_create_text_component_implements_interface(self):
        component = self.factory.create_text_component()
        self.assertTrue(isinstance(component, ITextComponent))


class TestTextComponentFactory(unittest.TestCase):
    def setUp(self):
        self.factory = BoldTextComponentFactory()

    def test_create_text_component(self):
        component = self.factory.create_text_component()
        self.assertIsInstance(component, BoldTextComponent)
        self.assertIsInstance(component, ITextComponent)

    def test_create_text_component_returns_new_instance(self):
        component1 = self.factory.create_text_component()
        component2 = self.factory.create_text_component()
        self.assertNotEqual(id(component1), id(component2))


class TestItalicTextComponentFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ItalicTextComponentFactory()

    def test_create_text_component_returns_italic_text_component(self):
        component = self.factory.create_text_component()
        self.assertIsInstance(component, ItalicTextComponent)

    def test_created_component_get_text_method(self):
        component = self.factory.create_text_component()
        self.assertTrue(callable(component.get_text))

class TestStrikethroughTextComponentFactory(unittest.TestCase):

    def setUp(self):
        self.factory = StrikethroughTextComponentFactory()

    def test_create_text_component_instance(self):
        component = self.factory.create_text_component()
        self.assertIsInstance(component, StrikethroughTextComponent)

    def test_create_text_component_interface(self):
        component = self.factory.create_text_component()
        self.assertTrue(isinstance(component, ITextComponent))

    def test_strikethrough_text_component_functionality(self):
        component = self.factory.create_text_component()
        text = component.get_text()
        self.assertIsInstance(text, str)


if __name__ == '__main__':
    unittest.main()
