import pypandoc

from .document import Document
from .md_document import MarkdownDocument
from ..text_component import TextComponent


class RichTextDocument(Document):
    def __init__(self):
        super().__init__()

    def from_dict(self,
                  data: dict) -> 'RichTextDocument':
        super().from_dict(data)

        return self


class MdToRichTextAdapter(RichTextDocument):
    def __init__(self,
                 md_document: MarkdownDocument):
        super().__init__()
        self.__md_document = md_document
        self._components = [TextComponent(self.get_text())]

    def get_text(self) -> str:
        text = self.__md_document.get_text()
        rtf_text = pypandoc.convert_text(text, 'rtf', 'md')

        if '{' not in rtf_text:
            rtf_text = r'{\rtf1}'
        else:
            rtf_text = rtf_text[:1] + r'\rtf1 ' + rtf_text[1:]

        return rtf_text
