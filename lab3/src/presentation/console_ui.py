import os

from ..application import StudentService
from ..application.commands import (
    AddStudentCommand,
    GetStudentsCommand,
    UpdateStudentCommand,
    GetStudentByIdCommand,
    ICommand,
)
from ..application.dto import StudentDTO
from ..application.quote_adapter import IQuoteService


class ConsoleUI(object):
    def __init__(
        self,
        student_service: StudentService,
        quote_adapter: IQuoteService,
    ):
        self.student_service = student_service
        self.quote_adapter = quote_adapter
        self.input_commands = {
            "add": self.add_student,
            "view": self.view_students,
            "edit": self.edit_student,
            "exit": self.exit,
        }

    def run(self):
        while True:
            print("\nCommands: add, view, edit, exit")
            command = input("Enter command: ").strip().lower()
            if command in self.input_commands:
                os.system("cls")
                self.input_commands[command]()
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
        self.execute_command(AddStudentCommand(self.student_service, student_dto))
        quote = self.quote_adapter.get_random_quote()
        print(
            f"\nStudent added. Here's a motivational quote:\n{quote.content} - {quote.author}"
        )

    def view_students(self):
        view_command = GetStudentsCommand(self.student_service)
        students = self.execute_command(view_command)
        if students:
            print(
                f"ID: {student.id_}, Name: {student.name}, Grade: {student.grade}"
                for student in students
            )
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

        get_command = GetStudentByIdCommand(self.student_service, student_id)
        student = self.execute_command(get_command)
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
            self.execute_command(
                UpdateStudentCommand(self.student_service, new_student_dto)
            )
            print("Student updated")
        else:
            print("Student not found")

    @staticmethod
    def execute_command(command: ICommand):
        return command.execute()

    @staticmethod
    def exit():
        exit()
