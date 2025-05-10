from abc import ABC, abstractmethod

from .abstractions import IStudent
from .student import Student


class IStudentFactory(ABC):
    @abstractmethod
    def create_student(self, name: str, grade: int) -> IStudent:
        pass


class StudentFactory(IStudentFactory):
    def create_student(self, name: str, grade: int) -> IStudent:
        return Student(id_=0, name=name, grade=grade)
