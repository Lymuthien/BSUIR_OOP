from .persistence.student_repository import StudentRepository
from .application.student_service import StudentService
from .application.quote_adapter import QuoteApiAdapter
from .presentation.console_ui import ConsoleUI


def main():
    repository = StudentRepository()
    service = StudentService(repository)
    quote_adapter = QuoteApiAdapter()
    ui = ConsoleUI(service, quote_adapter)
    ui.run()


if __name__ == "__main__":
    main()
