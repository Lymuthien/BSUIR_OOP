from .icommand import ICommand
from ...application.dto import StudentDTO


class EditStudentCommand(ICommand):
    def __init__(self, student_service):
        self._student_service = student_service

    def execute(self):
        while True:
            id_str = input("Enter student ID to edit: ").strip()
            try:
                student_id = int(id_str)
                break
            except ValueError:
                print("Invalid ID")

        student = self._student_service.get_student_by_id(student_id)
        if student:
            print(f"Current name: {student.name}, Current grade: {student.grade}")
            name = input("Enter new name (or press enter to keep current): ").strip()
            if not name:
                name = student.name

            while True:
                grade_str = input(
                    "Enter new grade (or press enter to keep current): "
                ).strip()
                if grade_str:
                    try:
                        grade = int(grade_str)
                        if 0 <= grade <= 10:
                            break
                        else:
                            print("Grade must be between 0 and 10")
                    except ValueError:
                        print("Invalid grade")
                else:
                    grade = student.grade
                    break

            new_student_dto = StudentDTO(name, grade, student_id)
            self._student_service.update_student(new_student_dto)
            print("Student updated")
        else:
            print("Student not found")
