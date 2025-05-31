import unittest

from lab3.src.domain.student import Student


class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student(id_=1, name="Alice", grade=8)

    def test_initialization(self):
        self.assertEqual(self.student.id, 1)
        self.assertEqual(self.student.name, "Alice")
        self.assertEqual(self.student.grade, 8)

    def test_name_validation_valid(self):
        self.student.name = "Bob"
        self.assertEqual(self.student.name, "Bob")

    def test_name_validation_empty(self):
        with self.assertRaises(ValueError) as context:
            self.student.name = ""
        self.assertEqual(str(context.exception), "Student name cannot be empty")

    def test_name_validation_non_string(self):
        with self.assertRaises(ValueError) as context:
            self.student.name = 123
        self.assertEqual(str(context.exception), "Student name must be a string")

    def test_grade_validation_valid(self):
        self.student.grade = 7
        self.assertEqual(self.student.grade, 7)

    def test_grade_validation_below_zero(self):
        with self.assertRaises(ValueError) as context:
            self.student.grade = -1
        self.assertEqual(
            str(context.exception), "Student grade must be between 0 and 10"
        )

    def test_grade_validation_above_ten(self):
        with self.assertRaises(ValueError) as context:
            self.student.grade = 11
        self.assertEqual(
            str(context.exception), "Student grade must be between 0 and 10"
        )

    def test_grade_validation_non_integer(self):
        with self.assertRaises(ValueError) as context:
            self.student.grade = "A"
        self.assertEqual(str(context.exception), "Student grade must be a integer")

    def test_to_dict(self):
        expected = {"id": 1, "name": "Alice", "grade": 8}
        self.assertEqual(self.student.to_dict(), expected)

    def test_from_dict(self):
        data = {"id": 2, "name": "Bob", "grade": 9}
        student = Student.from_dict(data)
        self.assertEqual(student.id, 2)
        self.assertEqual(student.name, "Bob")
        self.assertEqual(student.grade, 9)


if __name__ == "__main__":
    unittest.main()
