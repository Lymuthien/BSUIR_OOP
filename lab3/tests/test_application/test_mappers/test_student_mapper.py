import unittest

from lab3.src.application.dto.student_dto import StudentDTO
from lab3.src.application.mappers.student_mapper import (
    StudentMapper,
)
from lab3.src.domain.student import Student


class TestStudentMapper(unittest.TestCase):
    def test_to_dto(self):
        student = Student(id_=1, name="Alice", grade=8)

        dto = StudentMapper.to_dto(student)

        self.assertIsInstance(dto, StudentDTO)
        self.assertEqual(dto.id_, 1)
        self.assertEqual(dto.name, "Alice")
        self.assertEqual(dto.grade, 8)

    def test_from_dto(self):
        dto = StudentDTO(id_=2, name="Bob", grade=9)

        student = StudentMapper.from_dto(dto)

        self.assertIsInstance(student, Student)
        self.assertEqual(student.id, 2)
        self.assertEqual(student.name, "Bob")
        self.assertEqual(student.grade, 9)

    def test_bidirectional_conversion(self):
        original_student = Student(id_=3, name="Charlie", grade=7)

        dto = StudentMapper.to_dto(original_student)
        converted_student = StudentMapper.from_dto(dto)

        self.assertEqual(converted_student.id, original_student.id)
        self.assertEqual(converted_student.name, original_student.name)
        self.assertEqual(converted_student.grade, original_student.grade)


if __name__ == "__main__":
    unittest.main()
