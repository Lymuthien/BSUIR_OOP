from ..interfaces import ITextComponent


class TextComponent(ITextComponent):
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__.lower()] = cls

    def __init__(self,
                 text: str):
        self.__text: str = text

    @classmethod
    def registry(cls) -> dict:
        return cls._registry

    def get_text(self) -> str:
        return self.__text

    def to_dict(self) -> dict:
        return {
            'type': self.__class__.__name__,
            'text': self.__text
        }

    def from_dict(self,
                  data: dict) -> ITextComponent:
        self.__text = data['text']
        return self


class TextDecorator(TextComponent):
    def __init__(self,
                 text: str,
                 text_component: TextComponent):
        super().__init__(text)
        self._text_component: TextComponent = text_component

    @staticmethod
    def _can_decorate(text: str) -> bool:
        if text and text.count('*') != len(text):
            return True
        return False


class BoldTextComponent(TextDecorator):
    def __init__(self,
                 text_component: TextComponent = TextComponent('')):
        super().__init__(text_component.get_text(), text_component)

    def get_text(self) -> str:
        text = self._text_component.get_text()
        formatted_text = '\n'.join(map(lambda paragraph: f'**{paragraph}**' if self._can_decorate(paragraph)
        else paragraph, text.split('\n')))

        return formatted_text


class ItalicTextComponent(TextDecorator):
    def __init__(self,
                 text_component: TextComponent = TextComponent('')):
        super().__init__(text_component.get_text(), text_component)

    def get_text(self) -> str:
        text = self._text_component.get_text()
        formatted_text = '\n'.join(map(lambda paragraph: f'_{paragraph}_' if self._can_decorate(paragraph)
        else paragraph, text.split('\n')))

        return formatted_text


class StrikethroughTextComponent(TextDecorator):
    def __init__(self,
                 text_component: TextComponent = TextComponent('')):
        super().__init__(text_component.get_text(), text_component)

    def get_text(self) -> str:
        text = self._text_component.get_text()
        formatted_text = '\n'.join(map(lambda paragraph: f'~~{paragraph}~~' if self._can_decorate(paragraph)
        else paragraph, text.split('\n')))

        return formatted_text
