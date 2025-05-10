from ..student_service import StudentService
from lab3.domain.abstractions.iquote_gateway import IQuoteGateway


class AddStudentCommand(object):
    def __init__(self, student_service: StudentService, quote_adapter: IQuoteGateway):
        self.student_service = student_service
        self.quote_adapter = quote_adapter

    def execute(self, student_dto):
        self.student_service.add_student(student_dto)
        quote = self.quote_adapter.get_random_quote()
        return quote
