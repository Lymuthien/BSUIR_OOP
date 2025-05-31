from .icommand import ICommand
from ...application.dto import StudentDTO


class AddStudentCommand(ICommand):
    def __init__(self, student_service, quote_service):
        self._student_service = student_service
        self._quote_service = quote_service

    def execute(self):
        name = input("Enter name: ").strip()
        while not name:
            print("Name cannot be empty")
            name = input("Enter name: ").strip()

        while True:
            grade_str = input("Enter grade: ").strip()
            try:
                grade = int(grade_str)
                if 0 <= grade <= 10:
                    break
                else:
                    print("Grade must be between 0 and 10")
            except ValueError:
                print("Invalid grade")

        student_dto = StudentDTO(name, grade)
        self._student_service.add_student(student_dto)
        quote = self._quote_service.get_random_quote()
        print(f"\nStudent added. Here's a quote:\n{quote.content} - {quote.author}")
