import copy
import json
import os
from domain import Student, IStudentRepository


class StudentRepository(IStudentRepository):
    def __init__(self, file_path="students.json"):
        self.file_path = file_path
        self.students: list[Student] = []
        self.next_id = 1
        self.load()

    def get_all(self) -> list[Student]:
        return self.students.copy()

    def get_by_id(self, id_: int) -> Student | None:
        for student in self.students:
            if student.id == id_:
                return copy.deepcopy(student)
        return None

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.students = [Student.from_dict(item) for item in data]
                if self.students:
                    self.next_id = max(student.id for student in self.students) + 1
        else:
            self.students = []
            self.next_id = 1

    def save(self):
        with open(self.file_path, "w") as f:
            data = json.dumps([student.to_dict() for student in self.students])
            f.write(data)

    def add(self, student: Student):
        student.id = self.next_id
        self.students.append(student)
        self.next_id += 1
        self.save()

    def update(self, student: Student):
        for u_student in self.students:
            if u_student.id == student.id:
                u_student.name = student.name
                u_student.grade = student.grade
                self.save()
                return True
        return False

    def delete(self, student: Student):
        for u_student in self.students:
            if u_student.id == student.id:
                self.students.remove(u_student)
