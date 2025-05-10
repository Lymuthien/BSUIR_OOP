from lab3.application.dto.student_dto import StudentDTO
from lab3.domain.student import Student


class StudentMapper(object):
    @staticmethod
    def to_dto(student: Student) -> StudentDTO:
        return StudentDTO(id=student.id, name=student.name, grade=student.grade)

    @staticmethod
    def from_dto(dto: StudentDTO) -> Student:
        return Student(dto.id, dto.name, dto.grade)
