import json

from ..documents.plaintext_document import PlainTextToMdAdapter
from ..documents.richtext_document import RichTextToMdAdapter
from ...factories.generic_factory import GenericFactory
from ...factories.document_factory import DocumentFactory, documents
from ...interfaces import IDictable, ISerializer


class JsonSerializer(ISerializer):
    def serialize(self,
                  data) -> str:
        return json.dumps(data)

    def deserialize(self,
                    data: str):
        data_dict = json.loads(data)
        return data_dict

    @property
    def extension(self) -> str:
        return 'json'


class DocumentToJsonSerializerAdapter(JsonSerializer):
    def serialize(self,
                  data: IDictable = None) -> str:
        return super().serialize(data.to_dict())

    def deserialize(self,
                    data: str) -> IDictable:
        deserialized_data = super().deserialize(data)

        type_name = deserialized_data['type'].lower()
        doc = documents[type_name].create_document()

        doc = doc.from_dict(deserialized_data)
        if doc.__class__.__name__ == 'PlainTextDocument':
            return PlainTextToMdAdapter(doc)
        elif doc.__class__.__name__ == 'RichTextDocument':
            return RichTextToMdAdapter(doc)
        else:
            return doc
