from strip_markdown import strip_markdown

from .document import Document
from ..text_component import TextComponent, BoldTextComponent, ItalicTextComponent, StrikethroughTextComponent, \
    TextDecorator
from ..theme import Theme
from ...factories.generic_factory import GenericFactory


class MarkdownDocument(Document):
    def __init__(self):
        super().__init__()
        self._components.append(TextComponent(''))

    def _apply_style(self,
                     start: int,
                     end: int,
                     text_decorator: type[TextDecorator]):
        text = self.get_text()
        before = TextComponent(text[:start]) if start > 0 else None
        bold_part = text_decorator(TextComponent(text[start:end + 1]))
        after = TextComponent(text[end + 1:]) if end + 1 < len(text) else None

        self._components = [component for component in (before, bold_part, after) if component]
        self.notify()

    def set_theme(self,
                  theme: Theme):
        super().set_theme(theme)

        font = '#' * theme.font_size
        self._clear_from_style()

        new_text = TextComponent(self.get_text())
        if theme.bold:
            new_text = BoldTextComponent(new_text)
        if theme.italic:
            new_text = ItalicTextComponent(new_text)

        self._components = [TextComponent(font + ' ' + new_text.get_text().replace('\n', '\n' + font + ' '))]
        self.notify()

    def _clear_from_style(self):
        text_without_style = strip_markdown(self.get_text())
        self._components = [TextComponent(text_without_style)]

    def apply_bold(self,
                   start: int,
                   end: int) -> None:
        self._apply_style(start, end, BoldTextComponent)

    def apply_italic(self,
                     start: int,
                     end: int) -> None:
        self._apply_style(start, end, ItalicTextComponent)

    def apply_strikethrough(self,
                            start: int,
                            end: int) -> None:
        self._apply_style(start, end, StrikethroughTextComponent)

    def from_dict(self,
                  data: dict) -> 'MarkdownDocument':
        super().from_dict(data)

        self._components = []
        for component_data in data['components']:
            component = GenericFactory.create(component_data).from_dict(component_data)
            self._components.append(component)

        return self
