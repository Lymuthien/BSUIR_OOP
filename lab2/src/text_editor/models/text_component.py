from ..interfaces.itext_component import ITextComponent


class TextComponent(ITextComponent):
    def __init__(self, text: str):
        self.__text: str = text

    def get_text(self) -> str:
        return self.__text

    def get_formatted_text(self) -> str:
        return self.__text


class TextDecorator(TextComponent):
    def __init__(self, text, text_component: TextComponent):
        super().__init__(text)
        self._text_component: TextComponent = text_component


class BoldTextComponent(TextDecorator):
    def __init__(self, text_component: TextComponent):
        super().__init__(text_component.get_text(), text_component)

    def get_text(self) -> str:
        return self._text_component.get_text()

    def get_formatted_text(self) -> str:
        return f'**{self._text_component.get_formatted_text()}**'


class ItalicTextComponent(TextDecorator):
    def __init__(self, text_component: TextComponent):
        super().__init__(text_component.get_text(), text_component)

    def get_text(self) -> str:
        return self._text_component.get_text()

    def get_formatted_text(self) -> str:
        return f'*{self._text_component.get_formatted_text()}*'
