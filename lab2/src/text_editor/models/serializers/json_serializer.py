import json
from ...interfaces import ISerializer
from ...models.documents.document import Document
from ...models.documents.md_document import MarkdownDocument


class JsonSerializer(ISerializer):
    def serialize(self,
                  data) -> str:
        return json.dumps(data)

    def deserialize(self,
                    data: str):
        data_dict = json.loads(data)
        return data_dict

    def extension(self) -> str:
        return 'json'


class DocumentToJsonSerializerAdapter(JsonSerializer):
    def __init__(self,
                 document: Document):
        self.__document = document

    def serialize(self,
                  data: Document = None) -> str:
        doc = data if data is not None else self.__document
        return super().serialize(doc.to_dict())

    def deserialize(self,
                    data: str) -> Document:
        serialized_data = super().deserialize(data)

        return MarkdownDocument().from_dict(serialized_data)
