from abc import ABC, abstractmethod
from ..entity import Entity
from typing import TypeVar, Generic

T = TypeVar('T', bound=Entity)

class IRepository(Generic[T], ABC):
    @abstractmethod
    def get_by_id(self, id_: int) -> T:
        pass

    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def add(self, entity: T) -> None:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        pass
