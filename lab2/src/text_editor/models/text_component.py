from ..interfaces.itext_component import ITextComponent
from ..interfaces.iserializer import IDictable


class TextComponent(ITextComponent, IDictable):
    def __init__(self, text: str):
        self.__text: str = text

    def get_text(self) -> str:
        return self.__text

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'text': self.__text
        }

    def from_dict(self, data: dict) -> 'TextComponent':
        self.__text = data['text']
        return self


class TextDecorator(TextComponent):
    def __init__(self, text, text_component: TextComponent):
        super().__init__(text)
        self._text_component: TextComponent = text_component


class BoldTextComponent(TextDecorator):
    def __init__(self, text_component: TextComponent):
        super().__init__(text_component.get_text(), text_component)

    def get_text(self) -> str:
        return f'**{self._text_component.get_text()}**'


class ItalicTextComponent(TextDecorator):
    def __init__(self, text_component: TextComponent):
        super().__init__(text_component.get_text(), text_component)

    def get_text(self) -> str:
        return f'*{self._text_component.get_text()}*'
