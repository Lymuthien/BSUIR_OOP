from abc import abstractmethod, ABC

from ..interfaces import ITextComponent
from ..models.text_component import TextComponent, BoldTextComponent, ItalicTextComponent, StrikethroughTextComponent


class TextComponentFactory(ABC):
    @abstractmethod
    def create_text_component(self, data = None) -> ITextComponent: ...


class BasicTextComponentFactory(TextComponentFactory):
    def create_text_component(self, data: str = None) -> ITextComponent:
        return TextComponent(data) if data else TextComponent()


class BoldTextComponentFactory(TextComponentFactory):
    def create_text_component(self, data: ITextComponent = None) -> ITextComponent:
        return BoldTextComponent(data) if data else BoldTextComponent()


class ItalicTextComponentFactory(TextComponentFactory):
    def create_text_component(self, data: ITextComponent = None) -> ITextComponent:
        return ItalicTextComponent(data) if data else ItalicTextComponent()


class StrikethroughTextComponentFactory(TextComponentFactory):
    def create_text_component(self, data: ITextComponent = None) -> ITextComponent:
        return StrikethroughTextComponent(data) if data else StrikethroughTextComponent()


text_components: dict[str, TextComponentFactory] = {
    TextComponent.__name__.lower(): BasicTextComponentFactory(),
    BoldTextComponent.__name__.lower(): BoldTextComponentFactory(),
    ItalicTextComponent.__name__.lower(): ItalicTextComponentFactory(),
    StrikethroughTextComponent.__name__.lower(): StrikethroughTextComponentFactory(),
}
