from .icommand import ICommand
from ..student_service import StudentService


class GetStudentsCommand(ICommand):
    def __init__(self, student_service: StudentService):
        self._student_service = student_service

    def execute(self):
        return self._student_service.get_all_students()
