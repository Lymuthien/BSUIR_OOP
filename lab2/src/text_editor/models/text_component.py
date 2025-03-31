from abc import abstractmethod

from ..interfaces import ITextComponent


class TextComponent(ITextComponent):
    def __init__(self,
                 text: str = ''):
        self.__text: str = text

    def get_text(self) -> str:
        return self.__text

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'text': self.get_text()
        }

    def from_dict(self,
                  data: dict) -> ITextComponent:
        self.__text = data['text']
        return self


class TextDecorator(ITextComponent, Registrable):
    def __init__(self,
                 text_component: TextComponent):
        super().__init__()
        self._text_component: TextComponent = text_component

    @staticmethod
    def _can_decorate(text: str) -> bool:
        if text and text.count('*') != len(text):
            return True
        return False

    @abstractmethod
    def get_text(self) -> str: ...

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'text': self.get_text()
        }

    def from_dict(self,
                  data: dict) -> ITextComponent:
        self._text_component = TextComponent().from_dict(data)
        return self


class BoldTextComponent(TextDecorator):
    def __init__(self,
                 text_component: TextComponent = TextComponent()):
        super().__init__(text_component)

    def get_text(self) -> str:
        text = self._text_component.get_text()
        formatted_text = '\n'.join(map(lambda paragraph: f'**{paragraph}**' if self._can_decorate(paragraph)
        else paragraph, text.split('\n')))

        return formatted_text


class ItalicTextComponent(TextDecorator):
    def __init__(self,
                 text_component: TextComponent = TextComponent()):
        super().__init__(text_component)

    def get_text(self) -> str:
        text = self._text_component.get_text()
        formatted_text = '\n'.join(map(lambda paragraph: f'*{paragraph}*' if self._can_decorate(paragraph)
        else paragraph, text.split('\n')))

        return formatted_text


class StrikethroughTextComponent(TextDecorator):
    def __init__(self,
                 text_component: TextComponent = TextComponent()):
        super().__init__(text_component)

    def get_text(self) -> str:
        text = self._text_component.get_text()
        formatted_text = '\n'.join(map(lambda paragraph: f'~~{paragraph}~~' if self._can_decorate(paragraph)
        else paragraph, text.split('\n')))

        return formatted_text
