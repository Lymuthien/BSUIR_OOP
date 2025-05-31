import os

from .commands import (
    ExitCommand,
    EditStudentCommand,
    ViewStudentsCommand,
    AddStudentCommand,
    ICommand,
)
from ..application import StudentService
from ..domain.abstractions import IQuoteService


class ConsoleUI(object):
    def __init__(
        self,
        student_service: StudentService,
        quote_service: IQuoteService,
    ):
        self.student_service = student_service
        self.quote_service = quote_service
        self.input_commands: dict[str, ICommand] = {
            "add": AddStudentCommand(self.student_service, self.quote_service),
            "view": ViewStudentsCommand(self.student_service),
            "edit": EditStudentCommand(self.student_service),
            "exit": ExitCommand(),
        }

    def run(self):
        while True:
            print("\nCommands: add, view, edit, exit")
            command = input("Enter command: ").strip().lower()
            if command in self.input_commands:
                os.system("cls")
                self.input_commands[command].execute()
            else:
                print("Invalid command")
