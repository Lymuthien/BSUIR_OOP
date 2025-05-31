from abc import ABC, abstractmethod

from .istudent import IStudent


class IStudentRepository(ABC):
    @abstractmethod
    def get_by_id(self, id_: int) -> IStudent:
        pass

    @abstractmethod
    def get_all(self) -> list[IStudent]:
        pass

    @abstractmethod
    def add(self, student: IStudent) -> None:
        pass

    @abstractmethod
    def update(self, student: IStudent) -> None:
        pass

    @abstractmethod
    def delete(self, student: IStudent) -> None:
        pass
