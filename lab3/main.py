from persistence import StudentRepository
from application import StudentService
from application import QuoteApiAdapter
from presentation.console_ui import ConsoleUI


def main():
    repository = StudentRepository()
    service = StudentService(repository)
    quote_adapter = QuoteApiAdapter()
    ui = ConsoleUI(service, quote_adapter)
    ui.run()


if __name__ == "__main__":
    main()
