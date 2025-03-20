from ...interfaces import ISerializer
from ...models.documents.document import Document
from ...models.documents.md_document import MarkdownDocument


class TxtSerializer(ISerializer):
    def serialize(self,
                  data) -> str:
        return data

    def deserialize(self,
                    data: str):
        return data

    @property
    def extension(self) -> str:
        return 'txt'


class DocumentToTxtSerializerAdapter(TxtSerializer):
    def __init__(self,
                 document: Document):
        self.__document = document

    def serialize(self,
                  data: Document = None) -> str:
        doc = data if data is not None else self.__document
        text = doc.get_text()

        return super().serialize(text)

    def deserialize(self,
                    data: str) -> Document:
        serialized_data = super().deserialize(data)
        new_document = MarkdownDocument()
        new_document.insert_text(serialized_data, 0)

        return new_document