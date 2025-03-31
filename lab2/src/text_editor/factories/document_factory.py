from abc import abstractmethod, ABC

from ..interfaces import IDocument
from ..models.documents.md_document import MarkdownDocument
from ..models.documents.plaintext_document import PlainTextDocument
from ..models.documents.richtext_document import RichTextDocument


class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self) -> IDocument: ...


class MDFactory(DocumentFactory):
    def create_document(self) -> IDocument:
        return MarkdownDocument()


class RichTextFactory(DocumentFactory):
    def create_document(self) -> IDocument:
        return RichTextDocument()


class PlainTextFactory(DocumentFactory):
    def create_document(self) -> IDocument:
        return PlainTextDocument()


documents: dict[str, DocumentFactory] = {
    MarkdownDocument.__name__.lower(): MDFactory(),
    RichTextDocument.__name__.lower(): RichTextFactory(),
    PlainTextDocument.__name__.lower(): PlainTextFactory(),
}
