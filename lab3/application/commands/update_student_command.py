class UpdateStudentCommand:
    def __init__(self, student_service):
        self.student_service = student_service

    def execute(self, student_id, new_student_dto):
        self.student_service.update(student_id, new_student_dto)