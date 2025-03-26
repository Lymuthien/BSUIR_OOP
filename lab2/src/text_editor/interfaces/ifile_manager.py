from abc import ABC, abstractmethod

from ..interfaces.iserializer import ISerializer


class IFileManager(ABC):
    @abstractmethod
    def save(self,
             data,
             path: str,
             serializer: ISerializer,
             extension: str = None) -> None: ...

    @abstractmethod
    def load(self,
             path: str,
             serializer: ISerializer): ...

    @abstractmethod
    def delete(self,
               path: str): ...
