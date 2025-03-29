import json

from ...factories.generic_factory import GenericFactory
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

        doc = GenericFactory.create(deserialized_data)
        return doc.from_dict(deserialized_data)
