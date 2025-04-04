import pypandoc

from .document import Document
from .md_document import MarkdownDocument


class RichTextDocument(Document):
    def __init__(self):
        super().__init__()

    def from_dict(self,
                  data: dict) -> 'RichTextDocument':
        super().from_dict(data)

        return self


class MdToRichTextAdapter(RichTextDocument):
    def __init__(self,
                 md_document: MarkdownDocument = MarkdownDocument()):
        super().__init__()
        self.__md_document = md_document
        self._components = [
            self._basic_factory.create_text_component(self._convert_md_to_rich(md_document.get_text()))
        ]
        self._users = self.__md_document.users()

    @staticmethod
    def _convert_md_to_rich(text: str) -> str:
        rtf_text = pypandoc.convert_text(text, 'rtf', 'md')

        return rtf_text

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_['type'] = RichTextDocument.__name__

        return dict_


class RichTextToMdAdapter(MarkdownDocument):
    def __init__(self, rich_text_document: RichTextDocument | None = None):
        super().__init__()
        if rich_text_document is not None:
            self._components = [
                self._basic_factory.create_text_component(self._convert_rich_to_md(rich_text_document.get_text()))
            ]
            self._users = rich_text_document.users()

    @staticmethod
    def _convert_rich_to_md(rich_text: str) -> str:
        return pypandoc.convert_text(rich_text, 'md', 'rtf').replace('\r', '')

    def to_dict(self) -> dict:
        dict_ = super().to_dict()
        dict_['type'] = MarkdownDocument.__name__

        return dict_
