import os.path
import unittest
from unittest.mock import patch

from src.application.commands import AddStudentCommand
from src.application.quote_adapter import QuoteApiAdapter
from src.application import StudentService
from src.persistence import StudentRepository
from src.application.dto import StudentDTO


class TestApp(unittest.TestCase):
    def setUp(self):
        file_path = "fake_repo.json"
        if os.path.exists(file_path):
            os.remove(file_path)
        self.repository = StudentRepository(file_path)
        self.quote_adapter = QuoteApiAdapter()
        self.student_service = StudentService(self.repository)

    @patch.object(StudentRepository, "save")
    def test_add_student_success(self, mock_save):
        mock_save.return_value = None

        student_dto = StudentDTO(name="John Doe", grade=8)
        command = AddStudentCommand(self.student_service, student_dto)

        command.execute()

        students = self.repository.get_all()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].name, "John Doe")
        self.assertEqual(students[0].grade, 8)


if __name__ == "__main__":
    unittest.main()
