from abc import abstractmethod, ABC

from ..interfaces import ITextComponent
from ..models.text_component import TextComponent, BoldTextComponent, ItalicTextComponent, StrikethroughTextComponent


class TextComponentFactory(ABC):
    @abstractmethod
    def create_text_component(self) -> ITextComponent: ...


class BasicTextComponentFactory(TextComponentFactory):
    def create_text_component(self) -> ITextComponent:
        return TextComponent()


class BoldTextComponentFactory(TextComponentFactory):
    def create_text_component(self) -> ITextComponent:
        return BoldTextComponent()


class ItalicTextComponentFactory(TextComponentFactory):
    def create_text_component(self) -> ITextComponent:
        return ItalicTextComponent()


class StrikethroughTextComponentFactory(TextComponentFactory):
    def create_text_component(self) -> ITextComponent:
        return StrikethroughTextComponent()


text_components: dict[str, TextComponentFactory] = {
    TextComponent.__name__.lower(): BasicTextComponentFactory(),
    BoldTextComponent.__name__.lower(): BoldTextComponentFactory(),
    ItalicTextComponent.__name__.lower(): ItalicTextComponentFactory(),
    StrikethroughTextComponent.__name__.lower(): StrikethroughTextComponentFactory(),
}
