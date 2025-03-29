import json

from ...factories.generic_factory import GenericFactory
from ...interfaces import ISerializer
from ...models.documents.document import Document


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
    def __init__(self,
                 document: Document):
        self.__document = document

    def serialize(self,
                  data: Document = None) -> str:
        doc = data if data is not None else self.__document
        return super().serialize(doc.to_dict())

    def deserialize(self,
                    data: str):
        deserialized_data = super().deserialize(data)

        doc = GenericFactory.create(deserialized_data)
        return doc.from_dict(deserialized_data)
