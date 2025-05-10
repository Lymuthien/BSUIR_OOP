from .entity import Entity


class IStudent(Entity):
    pass


class Student(IStudent):
    def __init__(self, id_, name: str, grade: int):
        self.name = name
        self.grade = grade
        super().__init__(id_)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "grade": self.grade}

    @staticmethod
    def from_dict(data):
        return Student(data["id"], data["name"], data["grade"])
