from .dto.student_dto import StudentDTO
from .mappers import StudentMapper
from ..domain import StudentFactory, IStudentRepository, IStudentFactory


class StudentService(object):
    def __init__(self, repository: IStudentRepository):
        self._repository = repository
        self._mapper = StudentMapper()
        self._factory: IStudentFactory = StudentFactory()

    def add_student(self, student_dto: StudentDTO):
        student = self._factory.create_student(student_dto.name, student_dto.grade)
        self._repository.add(student)

    def update_student(self, student_dto: StudentDTO):
        student = self._mapper.from_dto(student_dto)
        self._repository.update(student)

    def get_all_students(self):
        students = self._repository.get_all()
        return [self._mapper.to_dto(student) for student in students]

    def get_student_by_id(self, student_id):
        student = self._repository.get_by_id(student_id)
        if student:
            return StudentDTO(student.name, student.grade, student.id)
        return None
