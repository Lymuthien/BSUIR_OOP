from .icommand import ICommand
from ..dto import StudentDTO
from ..student_service import StudentService


class UpdateStudentCommand(ICommand):
    def __init__(self, student_service: StudentService, student_dto: StudentDTO):
        self._student_service = student_service
        self._new_student_dto = student_dto

    def execute(self):
        self._student_service.update_student(self._new_student_dto)
