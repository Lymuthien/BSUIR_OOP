from ..application.commands import (
    AddStudentCommand,
    GetStudentsCommand,
    UpdateStudentCommand,
    GetStudentByIdCommand,
)
from ..application.dto import StudentDTO
from ..application.student_service import StudentService
from ..domain.abstractions import IQuoteGateway


class ConsoleUI(object):
    def __init__(self, student_service: StudentService, quote_adapter: IQuoteGateway):
        self.student_service = student_service
        self.quote_adapter = quote_adapter
        self.commands = {
            "add": self.add_student,
            "view": self.view_students,
            "edit": self.edit_student,
            "exit": self.exit,
        }

    def run(self):
        while True:
            print("\nCommands: add, view, edit, exit")
            command = input("Enter command: ").strip().lower()
            if command in self.commands:
                self.commands[command]()
            else:
                print("Invalid command")

    def add_student(self):
        name = input("Enter name: ").strip()
        while not name:
            print("Name cannot be empty")
            name = input("Enter name: ").strip()

        while True:
            grade_str = input("Enter grade: ").strip()
            try:
                grade = int(grade_str)
                if 1 <= grade <= 10:
                    break
                else:
                    print("Grade must be between 1 and 10")
            except ValueError:
                print("Invalid grade")

        student_dto = StudentDTO(name, grade)
        AddStudentCommand(self.student_service, student_dto).execute()
        quote = self.quote_adapter.get_random_quote()
        print(
            f"\nStudent added. Here's a motivational quote:\n{quote.content} - {quote.author}"
        )

    def view_students(self):
        view_command = GetStudentsCommand(self.student_service)
        students = view_command.execute()
        if students:
            for student in students:
                print(f"ID: {student.id}, Name: {student.name}, Grade: {student.grade}")
        else:
            print("No students found")

    def edit_student(self):
        while True:
            id_str = input("Enter student ID to edit: ").strip()
            try:
                student_id = int(id_str)
                break
            except ValueError:
                print("Invalid ID")

        student = GetStudentByIdCommand(self.student_service, student_id).execute()
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
                        if 0 < grade <= 10:
                            break
                        else:
                            print("Grade must be between 1 and 10")
                    except ValueError:
                        print("Invalid grade")
                else:
                    grade = student.grade
                    break

            new_student_dto = StudentDTO(name, grade, student_id)
            UpdateStudentCommand(self.student_service, new_student_dto).execute()
            print("Student updated")
        else:
            print("Student not found")

    @staticmethod
    def exit():
        print("Exiting...")
        exit()
