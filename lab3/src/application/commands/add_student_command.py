from ..dto import StudentDTO
from ..student_service import StudentService
from .icommand import ICommand


class AddStudentCommand(ICommand):
    def __init__(self, student_service: StudentService, student_dto: StudentDTO):
        self._student_service = student_service
        self._student_dto = student_dto

    def execute(self):
        self._student_service.add_student(self._student_dto)
