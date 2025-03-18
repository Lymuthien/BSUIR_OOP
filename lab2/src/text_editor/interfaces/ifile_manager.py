from abc import ABC, abstractmethod
from ..interfaces.iserializer import ISerializer


class IFileManager(ABC):
    @staticmethod
    @abstractmethod
    def save(data,
             path: str,
             serializer: ISerializer) -> None: ...

    @staticmethod
    @abstractmethod
    def load(path: str,
             serializer: ISerializer): ...
