from ..dto import StudentDTO
from ..student_service import StudentService
from .icommand import ICommand


class AddStudentCommand(ICommand):
    def __init__(self, student_service: StudentService, student_dto: StudentDTO):
        self.student_service = student_service
        self.student_dto = student_dto

    def execute(self):
        self.student_service.add_student(self.student_dto)
