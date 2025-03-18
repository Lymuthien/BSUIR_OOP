from strip_markdown import strip_markdown
from .document import Document
from ..text_component import TextComponent, BoldTextComponent, ItalicTextComponent
from ..theme import Theme


class MarkdownDocument(Document):
    def __init__(self):
        super().__init__()
        self._components.append(TextComponent(''))

    def set_theme(self,
                  theme: Theme):
        super().set_theme(theme)

        new_components = []
        font = '#' * self._settings.font_size
        bold = self._settings.all_bold
        italic = self._settings.all_italic

        self._clear_from_style()

        for component in self._components:
            new_component = TextComponent(component.get_text())
            if bold:
                new_component = BoldTextComponent(new_component)
            if italic:
                new_component = ItalicTextComponent(new_component)
            new_component = TextComponent(new_component.get_text().replace('\n', '\n' + font))
            new_components.append(new_component)

        self._components = new_components
        self.notify()

    def _clear_from_style(self):
        text_without_style = strip_markdown(self.get_text())
        self._components = [TextComponent(text_without_style)]

    def apply_bold(self,
                   start: int,
                   end: int) -> None:
        text = self.get_text()
        before = TextComponent(text[:start]) if start > 0 else None
        bold_part = BoldTextComponent(TextComponent(text[start:end + 1]))
        after = TextComponent(text[end + 1:]) if end + 1 < len(text) else None

        self._components = [component for component in (before, bold_part, after) if component]
        self.notify()

    def apply_italic(self,
                     start: int,
                     end: int) -> None:
        text = self.get_text()
        before = TextComponent(text[:start]) if start > 0 else None
        italic_part = ItalicTextComponent(TextComponent(text[start:end + 1]))
        after = TextComponent(text[end + 1:]) if end + 1 < len(text) else None

        self._components = [component for component in (before, italic_part, after) if component]
        self.notify()

    def from_dict(self,
                  data: dict) -> 'MarkdownDocument':
        self._components = []
        for component in data['components']:
            if component['type'] == 'TextComponent':
                self._components.append(TextComponent(component['text']))
            elif component['type'] == 'BoldTextComponent':
                self._components.append(BoldTextComponent(component['text']))
            elif component['type'] == 'ItalicTextComponent':
                self._components.append(ItalicTextComponent(component['text']))

        return self
