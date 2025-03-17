from ..interfaces.iserializer import ISerializer
from ..interfaces.ifile_manager import IFileManager

class LocalFileManager(IFileManager):
    @staticmethod
    def save(data, filename: str, serializer: ISerializer) -> None:
        serialized_data = serializer.serialize(data)
        filename += serializer.extension
        with open(filename, 'w') as file:
            file.write(serialized_data)

    @staticmethod
    def load(filename: str, serializer: ISerializer):
        with open(filename, 'r') as file:
            serialized_data = file.read()

        return serializer.deserialize(serialized_data)

