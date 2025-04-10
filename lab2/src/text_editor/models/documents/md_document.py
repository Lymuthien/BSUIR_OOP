import re

from strip_markdown import strip_markdown

from .document import Document
from ..theme import Theme
from ...factories.text_component_factory import text_components, BoldTextComponentFactory, ItalicTextComponentFactory, \
    TextComponentFactory, StrikethroughTextComponentFactory


class MarkdownDocument(Document):
    def __init__(self):
        super().__init__()
        self._style_factory: TextComponentFactory = BoldTextComponentFactory()
        self._components.append(self._basic_factory.create_text_component())

    def _apply_style(self,
                     start: int,
                     end: int,
                     factory: type[TextComponentFactory]):
        self._style_factory = factory()

        text = self.get_text()
        before = self._basic_factory.create_text_component(text[:start]) if start > 0 else None
        style_part = self._style_factory.create_text_component(
            self._basic_factory.create_text_component(text[start:end + 1])
        )
        after = self._basic_factory.create_text_component(text[end + 1:]) if end + 1 < len(text) else None

        self._components = [component for component in (before, style_part, after) if component is not None]
        self.notify()

    def set_theme(self,
                  theme: Theme):
        super().set_theme(theme)

        font = '#' * theme.font_size
        self._clear_from_style()

        new_text = self._basic_factory.create_text_component(self.get_text())
        if theme.bold:
            self._style_factory = BoldTextComponentFactory()
            new_text = self._style_factory.create_text_component(new_text)
        if theme.italic:
            self._style_factory = ItalicTextComponentFactory()
            new_text = self._style_factory.create_text_component(new_text)

        self._components = [self._basic_factory.create_text_component(
            font + ' ' + new_text.get_text().replace('\n', '\n\n' + font + ' ')), ]
        self.notify()

    def _clear_from_style(self):
        text_without_style = strip_markdown(self.get_text())
        text_without_style = re.sub(r'~~(.+?)~~', r'\1', text_without_style)
        self._components = [self._basic_factory.create_text_component(text_without_style)]

    def apply_bold(self,
                   start: int,
                   end: int) -> None:
        self._apply_style(start, end, BoldTextComponentFactory)

    def apply_italic(self,
                     start: int,
                     end: int) -> None:
        self._apply_style(start, end, ItalicTextComponentFactory)

    def apply_strikethrough(self,
                            start: int,
                            end: int) -> None:
        self._apply_style(start, end, StrikethroughTextComponentFactory)

    def from_dict(self,
                  data: dict) -> 'MarkdownDocument':

        super().from_dict(data)

        self._components = []
        for component_data in data['components']:
            type_name = component_data['type'].lower()
            component = text_components[type_name].create_text_component().from_dict(component_data)
            self._components.append(component)

        return self
