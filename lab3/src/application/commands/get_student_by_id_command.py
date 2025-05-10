from .icommand import ICommand
from ..student_service import StudentService


class GetStudentByIdCommand(ICommand):
    def __init__(self, student_service: StudentService, student_id: int):
        self.student_service = student_service
        self.student_id = student_id

    def execute(self):
        return self.student_service.get_student_by_id(self.student_id)
