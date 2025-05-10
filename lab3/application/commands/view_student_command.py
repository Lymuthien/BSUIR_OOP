from lab3.application.student_service import StudentService


class ViewStudentCommand:
    def __init__(self, student_service: StudentService):
        self.student_service = student_service

    def execute(self):
        return self.student_service.get_all_students()
