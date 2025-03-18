from strip_markdown import strip_markdown
from .document import Document
from .md_document import MarkdownDocument

from ..text_component import TextComponent


class PlainTextDocument(Document):
    def __init__(self):
        super().__init__()

    def from_dict(self, data: dict) -> 'PlainTextDocument':
        self._components = [TextComponent(component['text']) for component in data['components']]

        return self


class MdToPlainTextAdapter(PlainTextDocument):
    def __init__(self, md_document: MarkdownDocument):
        super().__init__()
        self.__md_document = md_document

    def get_text(self) -> str:
        text = self.__md_document.get_text()
        plane_text = strip_markdown(text)
        return plane_text
