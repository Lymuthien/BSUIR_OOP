import re

from strip_markdown import strip_markdown

from .document import Document
from .md_document import MarkdownDocument


class PlainTextDocument(Document):
    def __init__(self):
        super().__init__()

    def from_dict(self,
                  data: dict) -> 'PlainTextDocument':
        super().from_dict(data)

        return self


class MdToPlainTextAdapter(PlainTextDocument):
    def __init__(self,
                 md_document: MarkdownDocument = MarkdownDocument()):
        super().__init__()
        self.__md_document = md_document
        self._components = [
            self._basic_factory.create_text_component(self._convert_md_to_plain(md_document.get_text()))
        ]
        self._users = self.__md_document.users()

    @staticmethod
    def _convert_md_to_plain(text: str) -> str:
        plane_text = strip_markdown(text)
        plane_text = re.sub(r'~~(.*?)~~', r'\1', plane_text)
        return plane_text

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_['type'] = PlainTextDocument.__name__

        return dict_


class PlainTextToMdAdapter(MarkdownDocument):
    def __init__(self, plain_text_document: PlainTextDocument | None = None):
        super().__init__()
        if plain_text_document is not None:
            self._components = [self._basic_factory.create_text_component(plain_text_document.get_text())]
            self._users = plain_text_document.users()

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_['type'] = MarkdownDocument.__name__

        return dict_

