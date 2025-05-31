from src.application import StudentService
from src.infrastructure import StudentRepository, QuoteApiAdapter
from src.presentation.console_ui import ConsoleUI


def main():
    repository = StudentRepository()
    service = StudentService(repository)
    quote_adapter = QuoteApiAdapter()
    ui = ConsoleUI(service, quote_adapter)
    ui.run()


if __name__ == "__main__":
    main()
