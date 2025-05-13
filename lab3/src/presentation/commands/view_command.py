from .icommand import ICommand


class ViewStudentsCommand(ICommand):
    def __init__(self, student_service):
        self._student_service = student_service

    def execute(self):
        students = self._student_service.get_all_students()
        if students:
            for student in students:
                print(
                    f"ID: {student.id_}, Name: {student.name}, Grade: {student.grade}"
                )
        else:
            print("No students found")
