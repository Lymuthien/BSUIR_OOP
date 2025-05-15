import copy
import json
import os
from dataclasses import asdict

from ..application.dto import StudentDTO
from ..application.mappers import StudentMapper
from ..domain import Student, IStudentRepository


class StudentRepository(IStudentRepository):
    def __init__(self, file_path="students.json"):
        self._file_path = file_path
        self._students: list[Student] = []
        self._next_id = 1
        self._load()

    def get_all(self) -> list[Student]:
        return self._students.copy()

    def get_by_id(self, id_: int) -> Student | None:
        for student in self._students:
            if student.id == id_:
                return copy.deepcopy(student)
        return None

    def _load(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, "r") as f:
                data = json.load(f)
                self._students = [
                    StudentMapper.from_dto(StudentDTO(**item)) for item in data
                ]
                if self._students:
                    self._next_id = max(student.id for student in self._students) + 1
        else:
            self._students = []
            self._next_id = 1

    def save(self):
        with open(self._file_path, "w") as f:
            data = json.dumps(
                [asdict(StudentMapper.to_dto(student)) for student in self._students]
            )
            f.write(data)

    def add(self, student: Student):
        student.id = self._next_id
        self._students.append(student)
        self._next_id += 1
        self.save()

    def update(self, student: Student):
        for u_student in self._students:
            if u_student.id == student.id:
                u_student.name = student.name
                u_student.grade = student.grade
                self.save()
                return True
        return False

    def delete(self, student: Student):
        for u_student in self._students:
            if u_student.id == student.id:
                self._students.remove(u_student)
