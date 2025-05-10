from .entity import Entity


class Student(Entity):
    def __init__(self, id_, name: str, grade: int):
        self.name = name
        self.grade = grade
        super().__init__(id_)
