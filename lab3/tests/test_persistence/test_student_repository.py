import os
import unittest
from unittest.mock import patch

from lab3.src.domain.student import Student
from lab3.src.infrastructure.student_repository import StudentRepository


class TestStudentRepository(unittest.TestCase):
    def setUp(self):
        file_path = "fake_repo.json"
        if os.path.exists(file_path):
            os.remove(file_path)

        self.patcher_save = patch.object(StudentRepository, "save")

        self.mock_save = self.patcher_save.start()

        self.repo = StudentRepository(file_path)

    def tearDown(self):
        self.patcher_save.stop()

    def test_initialization(self):
        self.assertEqual(len(self.repo.get_all()), 0)

    def test_add_student(self):
        student = Student(id_=0, name="Test", grade=5)

        self.repo.add(student)

        self.assertEqual(len(self.repo.get_all()), 1)
        self.assertEqual(self.repo.get_by_id(1).name, "Test")
        self.mock_save.assert_called_once()

    def test_get_all(self):
        student1 = Student(id_=1, name="Alice", grade=8)
        student2 = Student(id_=2, name="Bob", grade=9)
        self.repo.add(student1)
        self.repo.add(student2)

        students = self.repo.get_all()

        self.assertEqual(len(students), 2)
        self.assertEqual(students[0].name, "Alice")
        self.assertEqual(students[1].name, "Bob")

    def test_get_by_id(self):
        student = Student(id_=1, name="Alice", grade=8)
        self.repo.add(student)

        found = self.repo.get_by_id(1)
        not_found = self.repo.get_by_id(99)

        self.assertEqual(found.name, "Alice")
        self.assertIsNone(not_found)

    def test_update_student(self):
        original = Student(id_=1, name="Alice", grade=8)
        self.repo.add(original)

        updated = Student(id_=1, name="Alice Updated", grade=9)
        self.repo.update(updated)

        self.assertEqual(self.repo.get_by_id(1).name, "Alice Updated")
        self.assertEqual(self.repo.get_by_id(1).grade, 9)
        self.mock_save.assert_called()

    def test_update_nonexistent(self):
        self.repo.update(Student(id_=99, name="Ghost", grade=0))
        self.mock_save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
