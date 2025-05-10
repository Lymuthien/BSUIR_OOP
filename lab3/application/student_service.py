from .dto.student_dto import StudentDTO
from .mappers import StudentMapper
from ..domain import StudentFactory, IStudentRepository, IStudentFactory


class StudentService(object):
    def __init__(self, repository: IStudentRepository):
        self.repository = repository
        self.mapper = StudentMapper()
        self.factory: IStudentFactory = StudentFactory()

    def add_student(self, student_dto: StudentDTO):
        student = self.factory.create_student(student_dto.name, student_dto.grade)
        self.repository.add(student)

    def update_student(self, student_id: int, student_dto: StudentDTO):
        student = self.mapper.from_dto(student_dto)
        student.id = student_id
        self.repository.update(student)

    def get_all_students(self):
        students = self.repository.get_all()
        return [self.mapper.to_dto(student) for student in students]

    def get_student_by_id(self, student_id):
        student = self.repository.get_by_id(student_id)
        if student:
            return StudentDTO(student.name, student.grade, student.id)
        return None
