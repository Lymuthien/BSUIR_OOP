from .document import Document
from ..text_component import TextComponent, BoldTextComponent, ItalicTextComponent


class MarkdownDocument(Document):
    def __init__(self):
        super().__init__()
        self._components.append(TextComponent(''))

    def apply_bold(self, start: int, end: int) -> None:
        text = self.get_text()
        before = TextComponent(text[:start]) if start > 0 else None
        bold_part = BoldTextComponent(TextComponent(text[start:end]))
        after = TextComponent(text[end:]) if end < len(text) else None

        self._components = [component for component in (before, bold_part, after) if component]
        self.notify()

    def apply_italic(self, start: int, end: int) -> None:
        text = self.get_text()
        before = TextComponent(text[:start]) if start > 0 else None
        italic_part = ItalicTextComponent(TextComponent(text[start:end]))
        after = TextComponent(text[end:]) if end < len(text) else None

        self._components = [component for component in (before, italic_part, after) if component]
        self.notify()
