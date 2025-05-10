from .student import Student, IStudent
from abc import ABC, abstractmethod


class IStudentFactory(ABC):
    @abstractmethod
    def create_student(self, id_: int, name: str, grade: int) -> IStudent:
        pass


class StudentFactory(IStudentFactory):
    def create_student(self, id_: int, name: str, grade: int) -> IStudent:
        return Student(id_, name, grade)
