from ..dto.student_dto import StudentDTO
from ...domain.student import Student, IStudent


class StudentMapper(object):
    @staticmethod
    def to_dto(student: IStudent) -> StudentDTO:
        return StudentDTO(name=student.name, grade=student.grade, id_=student.id)

    @staticmethod
    def from_dto(dto: StudentDTO) -> Student:
        return Student(dto.id_, dto.name, dto.grade)
